import secrets
from django.db import models
from accounts.models import Employee

PURPOSE_CHOICES = [
    ('official', 'Official Work'), ('personal', 'Personal Work'),
    ('medical', 'Medical Emergency'), ('bank', 'Bank Work'),
    ('government', 'Government Work'), ('other', 'Other'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('returned', 'Returned'),
]

TRANSPORT_CHOICES = [
    ('own_vehicle', 'Own Vehicle'), ('company_vehicle', 'Company Vehicle'),
    ('public_transport', 'Public Transport'), ('on_foot', 'On Foot'),
]

STAGE_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

# Workflow: role -> list of (stage_label, approver_role)
APPROVAL_WORKFLOW = {
    # Workflow 1: Employee creates → HOD → HR → Security
    'employee': [
        ('Department HOD Approval', 'department_hod'),
        ('HR Approval', 'hr'),
        ('Security Approval', 'security'),
    ],
    # Workflow 2: HOD/HR creates → President/Plant Head → HR → Security
    'department_hod': [
        ('President / Plant Head Approval', 'president_plant_head'),
        ('HR Approval', 'hr'),
        ('Security Approval', 'security'),
    ],
    'hr': [
        ('President / Plant Head Approval', 'president_plant_head'),
        ('HR Approval', 'hr'),
        ('Security Approval', 'security'),
    ],
    # Workflow 3: President/Plant Head creates → Management → Security
    'president_plant_head': [
        ('Management Approval', 'management'),
        ('Security Approval', 'security'),
    ],
    # Management/Admin/Security — direct approval (no workflow stages)
    'management':    [],
    'administrator': [],
    'security':      [],
}

# Roles that bypass workflow (full access)
BYPASS_ROLES = ('administrator', 'management', 'hr', 'security')


def get_workflow_stages(employee_role):
    return APPROVAL_WORKFLOW.get(employee_role, [])


class InternalGatePass(models.Model):
    pass_number = models.CharField(max_length=20, unique=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='internal_passes')
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    purpose_detail = models.TextField()
    destination = models.CharField(max_length=200, verbose_name='City')
    out_date = models.DateField()
    out_time = models.TimeField()
    expected_return_time = models.TimeField(null=True, blank=True)
    transport_mode = models.CharField(max_length=30, choices=TRANSPORT_CHOICES)
    vehicle_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    current_stage = models.PositiveSmallIntegerField(default=0)  # 0-based index into workflow
    # Final approver (security) stored here for backward compat
    approver = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_internal_passes')
    approval_remarks = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    actual_return_time = models.TimeField(null=True, blank=True)
    approval_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pass_number:
            from accounts.models import SystemSetting
            s = SystemSetting.get()
            self.pass_number = f'{s.igp_prefix}-{s.igp_next_number:05d}'
            s.igp_next_number += 1
            s.save(update_fields=['igp_next_number'])
        if not self.approval_token:
            self.approval_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def get_stages(self):
        return get_workflow_stages(self.employee.role)

    def total_stages(self):
        return len(self.get_stages())

    def __str__(self):
        return f"{self.pass_number} - {self.employee.employee_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internal Gate Pass'


class GatePassApproval(models.Model):
    gate_pass = models.ForeignKey(InternalGatePass, on_delete=models.CASCADE, related_name='approvals')
    stage = models.PositiveSmallIntegerField()           # 0-based stage index
    stage_label = models.CharField(max_length=100)       # e.g. "Dept HOD Approval"
    approver_role = models.CharField(max_length=30)      # role expected to approve
    approver = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='stage_approvals')
    status = models.CharField(max_length=20, choices=STAGE_STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    acted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['stage']
        unique_together = ('gate_pass', 'stage')
