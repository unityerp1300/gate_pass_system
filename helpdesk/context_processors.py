def helpdesk_context(request):
    if not request.user.is_authenticated:
        return {}
    try:
        from accounts.models import SystemSetting
        setting = SystemSetting.get()
        session_timeout_seconds = int(getattr(setting, 'session_timeout_minutes', 20) or 20) * 60
    except Exception:
        session_timeout_seconds = 20 * 60

    ctx = {'SESSION_TIMEOUT_SECONDS': session_timeout_seconds}

    try:
        from helpdesk.models import Ticket
        from helpdesk.views import _is_it
        user = request.user
        if _is_it(user):
            ctx['helpdesk_open_count'] = Ticket.objects.filter(status__in=['open', 'in_progress']).count()
            ctx['pending_hd_count'] = ctx['helpdesk_open_count']
        else:
            ctx['helpdesk_open_count'] = Ticket.objects.filter(raised_by=user, status__in=['open', 'in_progress']).count()
            ctx['pending_hd_count'] = 0
    except Exception:
        pass

    try:
        from internal_pass.models import InternalGatePass
        from django.db.models import Q
        user = request.user
        if user.is_superuser or user.has_role('administrator') or user.perm_igp_approve:
            ctx['pending_igp_count'] = InternalGatePass.objects.filter(status__in=['pending', 'in_progress']).count()
        else:
            ctx['pending_igp_count'] = 0
    except Exception:
        pass

    try:
        from visitor_pass.models import VisitorGatePass
        user = request.user
        if user.is_superuser or user.has_role('administrator') or user.perm_vgp_approve:
            ctx['pending_vgp_count'] = VisitorGatePass.objects.filter(status='pending').count()
        else:
            ctx['pending_vgp_count'] = 0
    except Exception:
        pass

    try:
        from material_pass.models import MaterialGatePass
        user = request.user
        if user.is_superuser or user.has_role('administrator') or user.perm_mgp_approve:
            ctx['pending_mgp_count'] = MaterialGatePass.objects.filter(status='pending').count()
        else:
            ctx['pending_mgp_count'] = 0
    except Exception:
        pass

    try:
        from grievance.models import Grievance
        user = request.user
        manage_roles = ('administrator', 'management', 'president_plant_head', 'department_hod', 'hr')
        if user.is_superuser or any(user.has_role(r) for r in manage_roles):
            ctx['pending_grv_count'] = Grievance.objects.filter(status__in=['open', 'under_review']).count()
        else:
            ctx['pending_grv_count'] = Grievance.objects.filter(raised_by=user, status__in=['open', 'under_review']).count()
    except Exception:
        pass

    return ctx
