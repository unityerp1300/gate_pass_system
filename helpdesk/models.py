from django.db import models
from accounts.models import Employee

PRIORITY_CHOICES = [
    ('low',      'Low'),
    ('medium',   'Medium'),
    ('high',     'High'),
    ('critical', 'Critical'),
]

STATUS_CHOICES = [
    ('open',        'Open'),
    ('in_progress', 'In Progress'),
    ('on_hold',     'On Hold'),
    ('resolved',    'Resolved'),
    ('closed',      'Closed'),
]

CATEGORY_CHOICES = [
    ('hardware',    'Hardware Issue'),
    ('software',    'Software Issue'),
    ('network',     'Network / Internet'),
    ('email',       'Email / Outlook'),
    ('printer',     'Printer / Scanner'),
    ('access',      'Access / Login'),
    ('cctv',        'CCTV'),
    ('other',       'Other'),
]

DOCTYPE_CHOICES = [
    ('incident', 'Incident'),
    ('service_request', 'Service Request'),
    ('access_request', 'Access Request'),
    ('change_request', 'Change Request'),
    ('other', 'Other'),
]


class Ticket(models.Model):
    ticket_number  = models.CharField(max_length=20, unique=True, editable=False)
    title          = models.CharField(max_length=200)
    description    = models.TextField()
    doc_type       = models.CharField(max_length=30, choices=DOCTYPE_CHOICES, default='incident', verbose_name='DocType')
    category       = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    priority       = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    raised_by      = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='raised_tickets')
    assigned_to    = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tickets')
    resolved_at    = models.DateTimeField(null=True, blank=True)
    resolution_note= models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            from accounts.models import SystemSetting
            setting = SystemSetting.get()
            self.ticket_number = f'{setting.tkt_prefix}-{setting.tkt_next_number:05d}'
            setting.tkt_next_number += 1
            setting.save(update_fields=['tkt_next_number'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ticket_number} — {self.title}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Help Desk Ticket'


class TicketComment(models.Model):
    ticket     = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ticket_comments')
    comment    = models.TextField()
    is_internal= models.BooleanField(default=False, verbose_name='Internal Note (IT only)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment on {self.ticket.ticket_number} by {self.author.username}'
