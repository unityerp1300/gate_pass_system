from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import JsonResponse
from datetime import timedelta

EXEMPT_PATHS = ('/accounts/login/', '/accounts/logout/', '/accounts/admin-otp/',
                '/accounts/reset-password/', '/accounts/session-check/',
                '/accounts/forgot-password/', '/accounts/inauguration/', '/maintenance/')

TRACK_PREFIXES = ('/internal-pass/', '/visitor-pass/', '/accounts/employees/',
                  '/accounts/settings/', '/dashboard/')


def _get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


def _module_from_path(path):
    if path.startswith('/internal-pass/'): return 'IGP'
    if path.startswith('/visitor-pass/'):  return 'VGP'
    if path.startswith('/accounts/employees/'): return 'Accounts'
    if path.startswith('/accounts/settings/'): return 'Settings'
    if path.startswith('/dashboard/'): return 'Dashboard'
    return 'System'


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # Paths that are NEVER blocked by maintenance mode
    MAINTENANCE_EXEMPT = (
        '/accounts/login/',
        '/accounts/logout/',
        '/accounts/admin-otp/',
        '/accounts/forgot-password/',
        '/accounts/session-check/',
        '/static/',
        '/media/',
    )

    def __call__(self, request):
        if not any(request.path.startswith(p) for p in self.MAINTENANCE_EXEMPT):
            try:
                from accounts.models import SystemSetting
                setting = SystemSetting.get()
                if setting.maintenance_mode:
                    # Only administrator / superuser can pass through
                    is_admin = (
                        request.user.is_authenticated and
                        (request.user.has_role('administrator') or request.user.is_superuser)
                    )
                    if not is_admin:
                        return render(request, 'maintenance.html',
                                      {'message': setting.maintenance_message}, status=503)
            except Exception:
                pass
        return self.get_response(request)


class SingleLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

            if not any(path.startswith(p) for p in EXEMPT_PATHS):

                # ── 1. Session timeout ────────────────────────────────────
                try:
                    from accounts.models import SystemSetting
                    SESSION_TIMEOUT_MINUTES = int(SystemSetting.get().session_timeout_minutes or 20)
                except Exception:
                    SESSION_TIMEOUT_MINUTES = 20

                last_activity = request.session.get('last_activity')
                if last_activity:
                    elapsed = timezone.now().timestamp() - last_activity
                    if elapsed > SESSION_TIMEOUT_MINUTES * 60:
                        self._log(request, 'session_timeout', _module_from_path(path),
                                  f'Session timed out after inactivity on {path}')
                        logout(request)
                        if is_ajax:
                            return JsonResponse({'timeout': True}, status=401)
                        return redirect(f'/accounts/login/?next={path}&reason=timeout')

                request.session['last_activity'] = timezone.now().timestamp()
                request.session.modified = True

                # ── 2. Single login check ─────────────────────────────────
                user = request.user
                stored_key = user.session_key
                current_key = request.session.session_key

                if stored_key and stored_key != current_key:
                    self._log(request, 'duplicate_kick', 'System',
                              f'Duplicate session detected. Kicked from {path}')
                    logout(request)
                    if is_ajax:
                        return JsonResponse({'kicked': True}, status=401)
                    return redirect('/accounts/login/?reason=duplicate')

                # ── 3. Track meaningful page views (GET only, non-AJAX) ───
                if (request.method == 'GET' and not is_ajax and
                        any(path.startswith(p) for p in TRACK_PREFIXES)):
                    self._log(request, 'page_view', _module_from_path(path),
                              f'Visited {path}')

        response = self.get_response(request)
        return response

    @staticmethod
    def _log(request, action, module, description):
        try:
            from accounts.models import AuditLog
            AuditLog.log(request, action=action, module=module, description=description)
        except Exception:
            pass


class InaugurationPageMiddleware:
    """
    Redirect authenticated users to a one-time inauguration page,
    controlled via System Settings and tracked per-user by version.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.user.is_authenticated:
                path = request.path or '/'
                # Skip for administrators and superusers
                if request.user.is_superuser or request.user.has_role('administrator'):
                    return self.get_response(request)
                if not any(path.startswith(p) for p in EXEMPT_PATHS) and not path.startswith('/static/') and not path.startswith('/media/'):
                    from accounts.models import SystemSetting, Employee
                    setting = SystemSetting.get()
                    if setting.welcome_enabled:
                        seen = int(getattr(request.user, 'welcome_seen_version', 0) or 0)
                        cur = int(setting.welcome_version or 1)
                        if seen < cur:
                            return redirect('/accounts/inauguration/')
        except Exception:
            pass
        return self.get_response(request)
