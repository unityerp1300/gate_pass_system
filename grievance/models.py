from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('salary', 'Salary / Payroll'),
    ('harassment', 'Harassment / Misconduct'),
    ('workload', 'Workload / Work Conditions'),
    ('leave', 'Leave / Attendance'),
    ('safety', 'Safety / HSEF'),
    ('promotion', 'Promotion / Appraisal'),
    ('facilities', 'Facilities / Infrastructure'),
    ('other', 'Other'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]

STATUS_CHOICES = [
    ('open', 'Open'),
    ('under_review', 'Under Review'),
    ('resolved', 'Resolved'),
    ('closed', 'Closed'),
]


class Grievance(models.Model):
    grievance_no   = models.CharField(max_length=20, unique=True, editable=False)
    raised_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grievances_raised')
    category       = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    priority       = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    subject        = models.CharField(max_length=200)
    description    = models.TextField()
    attachment     = models.FileField(upload_to='grievance_attachments/', blank=True, null=True)

    # Visibility flags — who this complaint is directed to
    notify_management    = models.BooleanField(default=True, verbose_name='Notify Management')
    notify_president     = models.BooleanField(default=True, verbose_name='Notify President / Plant Head')
    notify_hod           = models.BooleanField(default=True, verbose_name='Notify Department HOD')
    notify_hr            = models.BooleanField(default=True, verbose_name='Notify HR')

    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='grievances_assigned'
    )
    resolution_note = models.TextField(blank=True)
    resolved_at     = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Grievance'

    def __str__(self):
        return f'{self.grievance_no} — {self.subject}'


class GrievanceComment(models.Model):
    grievance  = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} on {self.grievance.grievance_no}'
