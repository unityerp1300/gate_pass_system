from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
import string
from django.utils import timezone
from datetime import timedelta

DEPARTMENT_CHOICES = [
    ('Management', 'Management'),
    ('Whole Plant', 'Whole Plant'),
    ('Administrator/ERP', 'Administrator/ERP'),
    ('Security', 'Security'),
    ('HR & Admin', 'HR & Admin'),
    ('HSEF', 'HSEF'),
    ('Mechanical (Crushing & Pyro)', 'Mechanical (Crushing & Pyro)'),
    ('Mechanical (Packing & Utility & Grinding)', 'Mechanical (Packing & Utility & Grinding)'),
    ('Electrical', 'Electrical'),
    ('Instrument', 'Instrument'),
    ('Process & Production', 'Process & Production'),
    ('QC', 'QC'),
    ('Civil', 'Civil'),
    ('IT', 'IT'),
    ('Purchase', 'Purchase'),
    ('Logistics', 'Logistics'),
    ('Store', 'Store'),
    ('Automobile', 'Automobile'),
    ('Account', 'Account'),
    ('Sales Account', 'Sales Account'),
    ('Sales', 'Sales'),
    ('Marketing', 'Marketing'),
]

ROLE_CHOICES = [
    ('administrator', 'Administrator'),
    ('management', 'Management'),
    ('president_plant_head', 'President-Plant Head'),
    ('department_hod', 'Department HOD'),
    ('hr', 'HR'),
    ('security', 'Security'),
    ('employee', 'Employee'),
]

FULL_ACCESS_ROLES = ('administrator', 'management')
MULTI_VALUE_SEPARATOR = '|'


class EmployeeManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrator')
        extra_fields.setdefault('employee_name', 'Super Admin')
        extra_fields.setdefault('employee_code', 'ADMIN001')
        extra_fields.setdefault('department', 'Administrator/ERP')
        extra_fields.setdefault('designation', 'System Administrator')
        return self.create_user(username, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    employee_name = models.CharField(max_length=100)
    employee_code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    additional_departments = models.TextField(blank=True, default='')
    designation = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')
    additional_roles = models.TextField(blank=True, default='')
    reporting_person = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')
    joining_date = models.DateField(null=True, blank=True)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    password_plain = models.CharField(max_length=128, blank=True)
    must_change_password = models.BooleanField(default=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # active session tracker
    welcome_seen_version = models.PositiveIntegerField(default=0)

    # ── Module Rights (granular) ──────────────────────────────────────────
    # Dashboard
    perm_dashboard_view   = models.BooleanField(default=True,  verbose_name='Dashboard View')

    # Accounts
    perm_accounts_view    = models.BooleanField(default=False, verbose_name='Accounts View')
    perm_accounts_write   = models.BooleanField(default=False, verbose_name='Accounts Write')
    perm_accounts_delete  = models.BooleanField(default=False, verbose_name='Accounts Delete')
    perm_accounts_export  = models.BooleanField(default=False, verbose_name='Accounts Export')

    # Internal Gate Pass
    perm_igp_view         = models.BooleanField(default=True,  verbose_name='IGP View')
    perm_igp_write        = models.BooleanField(default=True,  verbose_name='IGP Write')
    perm_igp_delete       = models.BooleanField(default=False, verbose_name='IGP Delete')
    perm_igp_approve      = models.BooleanField(default=False, verbose_name='IGP Approve/Reject')
    perm_igp_bypass       = models.BooleanField(default=False, verbose_name='IGP Bypass Approval')
    perm_igp_export       = models.BooleanField(default=False, verbose_name='IGP Export Reports')

    # Visitor Gate Pass
    perm_vgp_view         = models.BooleanField(default=True,  verbose_name='VGP View')
    perm_vgp_write        = models.BooleanField(default=True,  verbose_name='VGP Write')
    perm_vgp_delete       = models.BooleanField(default=False, verbose_name='VGP Delete')
    perm_vgp_approve      = models.BooleanField(default=False, verbose_name='VGP Approve/Reject')
    perm_vgp_bypass       = models.BooleanField(default=False, verbose_name='VGP Bypass Approval')
    perm_vgp_export       = models.BooleanField(default=False, verbose_name='VGP Export Reports')

    # IT Help Desk
    perm_helpdesk_view    = models.BooleanField(default=True,  verbose_name='Help Desk View')
    perm_helpdesk_write   = models.BooleanField(default=True,  verbose_name='Help Desk Raise Ticket')
    perm_helpdesk_manage  = models.BooleanField(default=False, verbose_name='Help Desk Manage (IT)')

    # Reports
    perm_reports_igp      = models.BooleanField(default=False, verbose_name='IGP Reports View')
    perm_reports_vgp      = models.BooleanField(default=False, verbose_name='VGP Reports View')
    perm_reports_mgp      = models.BooleanField(default=False, verbose_name='MGP Reports View')
    perm_reports_audit    = models.BooleanField(default=False, verbose_name='Audit Log View')

    # Material Gate Pass
    perm_mgp_view         = models.BooleanField(default=True,  verbose_name='MGP View')
    perm_mgp_write        = models.BooleanField(default=True,  verbose_name='MGP Write')
    perm_mgp_delete       = models.BooleanField(default=False, verbose_name='MGP Delete')
    perm_mgp_approve      = models.BooleanField(default=False, verbose_name='MGP Approve/Reject')
    perm_mgp_export       = models.BooleanField(default=False, verbose_name='MGP Export Reports')

    # Grievance Redressal
    perm_grv_view         = models.BooleanField(default=True,  verbose_name='Grievance View')
    perm_grv_write        = models.BooleanField(default=True,  verbose_name='Grievance Raise')
    perm_grv_manage       = models.BooleanField(default=False, verbose_name='Grievance Manage')

    # Separate granular
    perm_hd_raise         = models.BooleanField(default=True,  verbose_name='HD Raise Ticket')
    perm_mgp_request      = models.BooleanField(default=True,  verbose_name='MGP Request Raise')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    # ── Legacy aliases (backward compat) ─────────────────────────────────
    @property
    def can_access_dashboard(self):     return self.perm_dashboard_view
    @property
    def can_access_accounts(self):      return self.perm_accounts_view
    @property
    def can_access_internal_pass(self): return self.perm_igp_view
    @property
    def can_access_visitor_pass(self):  return self.perm_vgp_view
    @property
    def can_approve_internal_pass(self):return self.perm_igp_approve or self.perm_igp_bypass
    @property
    def can_approve_visitor_pass(self): return self.perm_vgp_approve or self.perm_vgp_bypass

    @staticmethod
    def _serialize_multi_values(values):
        cleaned = []
        for value in values or []:
            value = (value or '').strip()
            if value and value not in cleaned:
                cleaned.append(value)
        return ''.join(f'{MULTI_VALUE_SEPARATOR}{value}' for value in cleaned) + (MULTI_VALUE_SEPARATOR if cleaned else '')

    @staticmethod
    def _deserialize_multi_values(serialized):
        if not serialized:
            return []
        return [value for value in serialized.split(MULTI_VALUE_SEPARATOR) if value]

    def get_additional_departments(self):
        return self._deserialize_multi_values(self.additional_departments)

    def set_additional_departments(self, values):
        self.additional_departments = self._serialize_multi_values(values)

    def get_all_departments(self):
        return [self.department] + [value for value in self.get_additional_departments() if value != self.department]

    def has_department(self, department):
        return department in self.get_all_departments()

    def get_departments_display(self):
        labels = dict(DEPARTMENT_CHOICES)
        return ', '.join(labels.get(value, value) for value in self.get_all_departments())

    def get_additional_roles(self):
        return self._deserialize_multi_values(self.additional_roles)

    def set_additional_roles(self, values):
        self.additional_roles = self._serialize_multi_values(values)

    def get_all_roles(self):
        return [self.role] + [value for value in self.get_additional_roles() if value != self.role]

    def has_role(self, role):
        return role in self.get_all_roles()

    def get_roles_display(self):
        labels = dict(ROLE_CHOICES)
        return ', '.join(labels.get(value, value) for value in self.get_all_roles())

    def __str__(self):
        return f"{self.employee_name} ({self.employee_code})"

    class Meta:
        verbose_name = 'Employee'
        ordering = ['employee_name']


class SystemSetting(models.Model):
    """Singleton model — only one row ever exists (pk=1)."""
    igp_prefix = models.CharField(max_length=10, default='IGP', verbose_name='Internal Pass Prefix')
    igp_next_number = models.PositiveIntegerField(default=1, verbose_name='IGP Next Number')
    vgp_prefix = models.CharField(max_length=10, default='VGP', verbose_name='Visitor Pass Prefix')
    vgp_next_number = models.PositiveIntegerField(default=1, verbose_name='VGP Next Number')
    tkt_prefix = models.CharField(max_length=10, default='TKT', verbose_name='Ticket Prefix')
    tkt_next_number = models.PositiveIntegerField(default=1, verbose_name='Ticket Next Number')
    mgp_prefix = models.CharField(max_length=10, default='MGP', verbose_name='Material Pass Prefix')
    mgp_next_number = models.PositiveIntegerField(default=1, verbose_name='MGP Next Number')
    mr_prefix = models.CharField(max_length=10, default='MR', verbose_name='Material Request Prefix')
    mr_next_number = models.PositiveIntegerField(default=1, verbose_name='MR Next Number')
    grv_prefix = models.CharField(max_length=10, default='GRV', verbose_name='Grievance Prefix')
    grv_next_number = models.PositiveIntegerField(default=1, verbose_name='GRV Next Number')
    igp_print_fields = models.TextField(blank=True, default='', verbose_name='IGP Print Fields Config (JSON)')
    vgp_print_fields = models.TextField(blank=True, default='', verbose_name='VGP Print Fields Config (JSON)')
    mgp_print_fields = models.TextField(blank=True, default='', verbose_name='MGP Print Fields Config (JSON)')
    workflow_email_recipients = models.TextField(blank=True, default='', verbose_name='Workflow Email Recipients (JSON)')
    updated_at = models.DateTimeField(auto_now=True)

    # SMTP
    smtp_host     = models.CharField(max_length=100, default='smtp.gmail.com', blank=True)
    smtp_port     = models.PositiveIntegerField(default=587)
    smtp_use_tls  = models.BooleanField(default=True)
    smtp_user     = models.CharField(max_length=150, blank=True)
    smtp_password = models.CharField(max_length=200, blank=True)
    smtp_from     = models.CharField(max_length=200, blank=True)

    # Maintenance
    maintenance_mode    = models.BooleanField(default=False)
    maintenance_message = models.TextField(
        default='The Software is under maintenance. If you have any query kindly contact the ERP Department.',
        blank=True
    )

    # Session
    session_timeout_minutes = models.PositiveIntegerField(
        default=20,
        verbose_name='Session Timeout (minutes)',
        help_text='Inactivity timeout for all users (all roles).'
    )

    # Inauguration / Welcome page (one-time per user, versioned)
    welcome_enabled = models.BooleanField(default=False, verbose_name='Enable Inauguration Page')
    welcome_version = models.PositiveIntegerField(default=1, verbose_name='Inauguration Version')
    welcome_title = models.CharField(max_length=120, default='Welcome to the ERP System', blank=True)
    welcome_message_management = models.TextField(blank=True, default='A brief message from the entire Management Team.')
    welcome_message_president = models.TextField(blank=True, default='A brief message from the President-Plant Head.')

    # Workflow notification channels (single settings page control)
    notif_igp_popup = models.BooleanField(default=True, verbose_name='IGP Popup Notifications')
    notif_igp_email = models.BooleanField(default=True, verbose_name='IGP Email Notifications')
    notif_vgp_popup = models.BooleanField(default=True, verbose_name='VGP Popup Notifications')
    notif_vgp_email = models.BooleanField(default=True, verbose_name='VGP Email Notifications')
    notif_mgp_popup = models.BooleanField(default=True, verbose_name='MGP Popup Notifications')
    notif_mgp_email = models.BooleanField(default=True, verbose_name='MGP Email Notifications')
    notif_hd_popup = models.BooleanField(default=True, verbose_name='HD Popup Notifications')
    notif_hd_email = models.BooleanField(default=True, verbose_name='HD Email Notifications')
    
    # Workflow configuration controls
    skip_management_notifications = models.BooleanField(
        default=False,
        verbose_name='Skip Management Notifications',
        help_text='If enabled, Management role will not receive routine notifications (approval-required only)'
    )
    skip_plant_head_notifications = models.BooleanField(
        default=False,
        verbose_name='Skip Plant Head Notifications',
        help_text='If enabled, Plant Head role will not receive routine notifications (approval-required only)'
    )

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'System Settings'

    class Meta:
        verbose_name = 'System Setting'


class RoleModuleAccess(models.Model):
    """Controls which modules (IGP/VGP/HD) are visible per role (non-admin roles only)."""
    EXCLUDED_ROLES = ('administrator', 'management', 'president_plant_head')
    role         = models.CharField(max_length=30, choices=ROLE_CHOICES, unique=True)
    show_igp     = models.BooleanField(default=True,  verbose_name='Show IGP')
    show_vgp     = models.BooleanField(default=True,  verbose_name='Show VGP')
    show_hd      = models.BooleanField(default=True,  verbose_name='Show Help Desk')

    @classmethod
    def get_for_role(cls, role):
        obj, _ = cls.objects.get_or_create(role=role, defaults={'show_igp': True, 'show_vgp': True, 'show_hd': True})
        return obj

    def __str__(self):
        return f'Module Access: {self.get_role_display()}'

    class Meta:
        verbose_name = 'Role Module Access'


class RolePermissionTemplate(models.Model):
    """Stores default permission sets per role. Used in Settings page."""
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, unique=True)

    perm_dashboard_view  = models.BooleanField(default=True)
    perm_accounts_view   = models.BooleanField(default=False)
    perm_accounts_write  = models.BooleanField(default=False)
    perm_accounts_delete = models.BooleanField(default=False)
    perm_accounts_export = models.BooleanField(default=False)
    perm_igp_view        = models.BooleanField(default=True)
    perm_igp_write       = models.BooleanField(default=True)
    perm_igp_delete      = models.BooleanField(default=False)
    perm_igp_approve     = models.BooleanField(default=False)
    perm_igp_bypass      = models.BooleanField(default=False)
    perm_igp_export      = models.BooleanField(default=False)
    perm_vgp_view        = models.BooleanField(default=True)
    perm_vgp_write       = models.BooleanField(default=True)
    perm_vgp_delete      = models.BooleanField(default=False)
    perm_vgp_approve     = models.BooleanField(default=False)
    perm_vgp_bypass      = models.BooleanField(default=False)
    perm_vgp_export      = models.BooleanField(default=False)
    perm_helpdesk_view   = models.BooleanField(default=True)
    perm_helpdesk_write  = models.BooleanField(default=True)
    perm_helpdesk_manage = models.BooleanField(default=False)
    perm_reports_igp     = models.BooleanField(default=False)
    perm_reports_vgp     = models.BooleanField(default=False)
    perm_reports_mgp     = models.BooleanField(default=False)
    perm_reports_audit   = models.BooleanField(default=False)
    perm_mgp_view        = models.BooleanField(default=True)
    perm_mgp_write       = models.BooleanField(default=True)
    perm_mgp_delete      = models.BooleanField(default=False)
    perm_mgp_approve     = models.BooleanField(default=False)
    perm_mgp_export      = models.BooleanField(default=False)
    perm_grv_view        = models.BooleanField(default=True)
    perm_grv_write       = models.BooleanField(default=True)
    perm_grv_manage      = models.BooleanField(default=False)
    perm_hd_raise        = models.BooleanField(default=True)
    perm_mgp_request     = models.BooleanField(default=True)

    PERM_FIELDS = [
        'perm_dashboard_view',
        'perm_accounts_view','perm_accounts_write','perm_accounts_delete','perm_accounts_export',
        'perm_igp_view','perm_igp_write','perm_igp_delete','perm_igp_approve','perm_igp_bypass','perm_igp_export',
        'perm_vgp_view','perm_vgp_write','perm_vgp_delete','perm_vgp_approve','perm_vgp_bypass','perm_vgp_export',
        'perm_helpdesk_view','perm_helpdesk_write','perm_helpdesk_manage',
        'perm_reports_igp','perm_reports_vgp','perm_reports_mgp','perm_reports_audit',
        'perm_mgp_view','perm_mgp_write','perm_mgp_delete','perm_mgp_approve','perm_mgp_export',
        'perm_grv_view','perm_grv_write','perm_grv_manage',
        'perm_hd_raise','perm_mgp_request',
    ]

    def apply_to(self, employee):
        """Copy this template's permissions onto an employee instance."""
        for f in self.PERM_FIELDS:
            setattr(employee, f, getattr(self, f))

    def __str__(self):
        return f'Permissions: {self.get_role_display()}'

    class Meta:
        verbose_name = 'Role Permission Template'


class AdminOTPSession(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='otp_session')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    @classmethod
    def generate_for(cls, employee):
        code = ''.join(random.choices(string.digits, k=6))
        obj, _ = cls.objects.update_or_create(
            employee=employee,
            defaults={'otp_code': code, 'verified': False}
        )
        return obj

    def __str__(self):
        return f'OTP for {self.employee.username}'


ACTION_CHOICES = [
    ('login',           'Login'),
    ('logout',          'Logout'),
    ('login_failed',    'Login Failed'),
    ('otp_verified',    'OTP Verified'),
    ('session_timeout', 'Session Timeout'),
    ('duplicate_kick',  'Duplicate Session Kicked'),
    ('igp_create',      'IGP Created'),
    ('igp_approve',     'IGP Approved'),
    ('igp_reject',      'IGP Rejected'),
    ('igp_return',      'IGP Returned'),
    ('vgp_create',      'VGP Created'),
    ('vgp_approve',     'VGP Approved'),
    ('vgp_reject',      'VGP Rejected'),
    ('vgp_checkout',    'VGP Checked Out'),
    ('employee_create', 'Employee Created'),
    ('employee_edit',   'Employee Edited'),
    ('employee_delete', 'Employee Deleted'),
    ('settings_change', 'Settings Changed'),
    ('password_reset',  'Password Reset'),
    ('page_view',       'Page View'),
    ('mgp_create',      'MGP Created'),
    ('mgp_approve',     'MGP Approved'),
    ('mgp_reject',      'MGP Rejected'),
    ('mgp_return',      'MGP Returned'),
]


class AuditLog(models.Model):
    user        = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_logs')
    username    = models.CharField(max_length=50, blank=True)   # keep even if user deleted
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    hostname    = models.CharField(max_length=200, blank=True, verbose_name='Desktop/Hostname')
    action      = models.CharField(max_length=30, choices=ACTION_CHOICES)
    module      = models.CharField(max_length=50, blank=True)   # e.g. IGP, VGP, Accounts
    description = models.TextField(blank=True)                  # human-readable detail
    extra       = models.JSONField(default=dict, blank=True)    # any extra structured data
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'

    def __str__(self):
        return f'[{self.timestamp:%d-%m-%Y %H:%M}] {self.username} — {self.action}'

    @classmethod
    def log(cls, request, action, module='', description='', extra=None, user=None):
        try:
            u = user or (request.user if request and request.user.is_authenticated else None)
            ip = cls._get_ip(request)
            cls.objects.create(
                user=u,
                username=u.username if u else '',
                ip_address=ip,
                hostname=request.session.get('client_hostname', '') if request else '',
                action=action,
                module=module,
                description=description,
                extra=extra or {},
            )
            # Auto-remove logs older than 1 day
            cls.objects.filter(timestamp__lt=timezone.now() - timedelta(days=1)).delete()
        except Exception:
            pass

    @staticmethod
    def _get_ip(request):
        if not request:
            return None
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


class Notification(models.Model):
    """System notifications for pass approvals, rejections, and help desk actions."""
    NOTIFICATION_TYPES = [
        ('igp_approved', 'IGP Approved'),
        ('igp_rejected', 'IGP Rejected'),
        ('vgp_approved', 'VGP Approved'),
        ('vgp_rejected', 'VGP Rejected'),
        ('mgp_approved', 'MGP Approved'),
        ('mgp_rejected', 'MGP Rejected'),
        ('hd_resolved', 'Ticket Resolved'),
        ('hd_assigned', 'Ticket Assigned'),
    ]
    
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    related_id = models.CharField(max_length=50, blank=True)
    related_module = models.CharField(max_length=20, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
    
    def __str__(self):
        return f'{self.recipient.username} — {self.get_notification_type_display()}'
    
    @classmethod
    def create(cls, recipient, notification_type, title, description='', related_id='', related_module=''):
        """Create a notification for a user."""
        return cls.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            description=description,
            related_id=related_id,
            related_module=related_module,
        )
    
    @classmethod
    def get_unread_count(cls, user):
        """Get count of unread notifications for a user."""
        return cls.objects.filter(recipient=user, is_read=False).count()
    
    @classmethod
    def get_recent(cls, user, limit=10):
        """Get recent unread notifications for a user."""
        return cls.objects.filter(recipient=user).order_by('-created_at')[:limit]


class EmailLog(models.Model):
    """Stores outgoing email delivery attempts for audit and troubleshooting."""
    CHANNEL_CHOICES = [
        ('igp', 'IGP'),
        ('vgp', 'VGP'),
        ('mgp', 'MGP'),
        ('hd', 'Help Desk'),
        ('system', 'System'),
    ]

    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='system')
    status = models.CharField(max_length=20, default='sent')  # sent | failed | skipped
    related_id = models.CharField(max_length=50, blank=True)
    related_module = models.CharField(max_length=20, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Log'

    def __str__(self):
        return f'{self.recipient} — {self.subject} ({self.status})'


class NotificationPermission(models.Model):
    """Controls which roles/employees/departments can receive and see which notifications."""
    NOTIFICATION_TYPES = [
        ('igp_approved', 'IGP Approved'),
        ('igp_rejected', 'IGP Rejected'),
        ('vgp_approved', 'VGP Approved'),
        ('vgp_rejected', 'VGP Rejected'),
        ('mgp_approved', 'MGP Approved'),
        ('mgp_rejected', 'MGP Rejected'),
        ('hd_resolved', 'Ticket Resolved'),
        ('hd_assigned', 'Ticket Assigned'),
        ('all', 'All Notifications'),
    ]
    
    SCOPE_CHOICES = [
        ('role', 'By Role'),
        ('employee', 'By Employee'),
        ('department', 'By Department'),
    ]
    
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, help_text="Scope of this permission")
    role = models.CharField(max_length=50, blank=True, help_text="Role (if scope=role)")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, help_text="Employee (if scope=employee)")
    department = models.CharField(max_length=100, blank=True, choices=DEPARTMENT_CHOICES, help_text="Department (if scope=department)")
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, help_text="Which notification type is allowed")
    can_receive = models.BooleanField(default=True, help_text="Can this group receive this notification type?")
    can_view_own = models.BooleanField(default=True, help_text="Can view their own notifications?")
    can_view_department = models.BooleanField(default=False, help_text="Can view department notifications?")
    can_view_all = models.BooleanField(default=False, help_text="Can view all notifications?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('scope', 'role', 'employee', 'department', 'notification_type')
        verbose_name = 'Notification Permission'
        verbose_name_plural = 'Notification Permissions'
    
    def __str__(self):
        if self.scope == 'role':
            target = f"Role: {self.role}"
        elif self.scope == 'employee':
            target = f"Employee: {self.employee.username}"
        else:
            target = f"Department: {self.department}"
        return f"{target} — {self.get_notification_type_display()}"
    
    @classmethod
    def can_user_receive(cls, user, notification_type):
        """Check if user can receive a specific notification type."""
        # Superuser bypasses permission rules.
        if user.is_superuser:
            return True
        
        # Check employee-level permission
        emp_perm = cls.objects.filter(scope='employee', employee=user, notification_type=notification_type).first()
        if emp_perm:
            return emp_perm.can_receive
        
        # Check role-level permission
        for role in user.get_all_roles():
            role_perm = cls.objects.filter(scope='role', role=role, notification_type=notification_type).first()
            if role_perm:
                return role_perm.can_receive
        
        # Check department-level permission
        for department in user.get_all_departments():
            dept_perm = cls.objects.filter(scope='department', department=department, notification_type=notification_type).first()
            if dept_perm:
                return dept_perm.can_receive
        
        # Default: allow
        return True
    
    @classmethod
    def get_visible_notifications(cls, user):
        """Get notifications visible to this user using fixed system rules."""
        
        if user.is_superuser:
            return Notification.objects.all().order_by('-created_at')

        full_access_roles = ('administrator', 'management', 'president_plant_head', 'hr', 'security')
        if any(user.has_role(role) for role in full_access_roles):
            return Notification.objects.all().order_by('-created_at')

        if user.has_department('IT'):
            allowed_types = ('hd_resolved', 'hd_assigned')
        else:
            allowed_types = (
                'igp_approved', 'igp_rejected',
                'vgp_approved', 'vgp_rejected',
                'mgp_approved', 'mgp_rejected',
                'hd_resolved', 'hd_assigned',
            )

        dept_q = Q(recipient__department__in=user.get_all_departments())
        extra_dept_q = Q()
        for department in user.get_all_departments():
            extra_dept_q |= Q(recipient__additional_departments__contains=f'{MULTI_VALUE_SEPARATOR}{department}{MULTI_VALUE_SEPARATOR}')

        return Notification.objects.filter(
            (dept_q | extra_dept_q),
            notification_type__in=allowed_types,
        ).order_by('-created_at')


class NotificationWorkflow(models.Model):
    PASS_TYPE_CHOICES = [
        ('igp', 'Internal Gate Pass (IGP)'),
        ('vgp', 'Visitor Gate Pass (VGP)'),
        ('mgp', 'Material Gate Pass (MGP)'),
        ('helpdesk', 'IT Help Desk'),
    ]
    
    CREATOR_ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('department_hod', 'Department HOD/HR'),
        ('plant_head', 'Plant Head'),
        ('security', 'Security'),
        ('management', 'Management'),
        ('any', 'Any Role (Default)'),
    ]
    
    pass_type = models.CharField(max_length=20, choices=PASS_TYPE_CHOICES)
    creator_role = models.CharField(
        max_length=50, 
        choices=CREATOR_ROLE_CHOICES, 
        default='any',
        help_text="Which role creates the pass - determines which workflow to use"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Workflow'
        verbose_name_plural = 'Notification Workflows'
        unique_together = ('pass_type', 'creator_role')
    
    def __str__(self):
        if self.creator_role == 'any':
            return f"{self.get_pass_type_display()} Workflow - {self.name}"
        return f"{self.get_pass_type_display()} ({self.get_creator_role_display()}) - {self.name}"


class WorkflowStage(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('popup', 'Popup Notification'),
        ('email', 'Email Notification'),
        ('both', 'Both Popup & Email'),
        ('none', 'None (Disabled)'),
    ]
    
    workflow = models.ForeignKey(NotificationWorkflow, on_delete=models.CASCADE, related_name='stages')
    stage_number = models.IntegerField(help_text="Order of stages (1=first, 2=second, etc.)")
    stage_name = models.CharField(max_length=100, help_text="e.g., 'Department HOD Approval', 'Contact Person Approval'")
    description = models.TextField(blank=True)
    
    approver_role = models.CharField(max_length=50, blank=True, help_text="Role required to approve (e.g., 'department_hod', 'security'). Leave blank if not approval stage.")
    is_approval_stage = models.BooleanField(default=False, help_text="Is this an approval stage or just notification?")
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='both')
    
    send_to_roles = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Comma-separated roles to notify (e.g., 'department_hod,security')"
    )
    
    send_to_employee = models.BooleanField(default=True, help_text="Send notification to pass requester/creator")
    
    skip_for_management = models.BooleanField(
        default=False, 
        help_text="Don't send notification if approver is Management role"
    )
    skip_for_plant_head = models.BooleanField(
        default=False, 
        help_text="Don't send notification if approver is Plant Head role"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('workflow', 'stage_number')
        ordering = ['workflow', 'stage_number']
    
    def __str__(self):
        return f"{self.workflow.get_pass_type_display()} - Stage {self.stage_number}: {self.stage_name}"
    
    def get_notification_roles(self):
        """Returns list of roles to notify for this stage"""
        if not self.send_to_roles:
            return []
        return [role.strip() for role in self.send_to_roles.split(',')]


class WorkflowNotificationRecipient(models.Model):
    """Allows fine-grained control over who receives notifications at each stage"""
    
    stage = models.ForeignKey(WorkflowStage, on_delete=models.CASCADE, related_name='extra_recipients')
    recipient_role = models.CharField(max_length=50, help_text="Role that should receive notifications")
    is_optional = models.BooleanField(default=False, help_text="Is this a CC/optional recipient?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('stage', 'recipient_role')
    
    def __str__(self):
        return f"{self.stage.stage_name} -> {self.recipient_role}"
