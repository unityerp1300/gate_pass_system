import uuid
from django.db import models
from accounts.models import Employee

VISIT_PURPOSE_CHOICES = [
    ('business_meeting', 'Business Meeting'), ('vendor', 'Vendor/Supplier'),
    ('interview', 'Interview'), ('audit', 'Audit/Inspection'),
    ('delivery', 'Delivery'), ('maintenance', 'Maintenance/Repair'),
    ('industry_visit', 'Industry Visit'), ('other', 'Other'),
]

VISITOR_STATUS_CHOICES = [
    ('pending', 'Pending'), ('approved', 'Approved'),
    ('rejected', 'Rejected'), ('checked_out', 'Checked Out'),
]

ID_TYPE_CHOICES = [
    ('aadhar', 'Aadhar Card'), ('pan', 'PAN Card'), ('passport', 'Passport'),
    ('driving_license', 'Driving License'), ('voter_id', 'Voter ID'), ('other', 'Other'),
]

MATERIAL_CATEGORY_CHOICES = [
    ('returnable', 'Returnable'),
    ('non_returnable', 'Non-Returnable'),
]


class VisitorGatePass(models.Model):
    pass_number = models.CharField(max_length=20, unique=True, editable=False)
    visitor_name = models.CharField(max_length=100)
    visitor_company = models.CharField(max_length=200, blank=True, verbose_name='Organization')
    visitor_city = models.CharField(max_length=200, blank=True, verbose_name='City')
    visitor_phone = models.CharField(max_length=15, verbose_name='Visitor Mobile Number')
    visitor_email = models.EmailField(blank=True)
    id_type = models.CharField(max_length=30, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=50)
    no_of_visitors = models.PositiveIntegerField(default=1)
    visit_purpose = models.CharField(max_length=50, choices=VISIT_PURPOSE_CHOICES, verbose_name='Purpose')
    visit_detail = models.TextField()
    material = models.CharField(max_length=200, blank=True, verbose_name='Material')
    material_category = models.CharField(max_length=20, choices=MATERIAL_CATEGORY_CHOICES,
                                         blank=True, verbose_name='Material Category')
    access_card_no = models.CharField(max_length=50, blank=True, verbose_name='Access Card No.')
    person_to_meet = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                       related_name='visitor_passes', verbose_name='Contact Person')
    visit_date = models.DateField()
    in_time = models.TimeField(verbose_name='In Time')
    expected_out_time = models.TimeField(verbose_name='Out Time')
    vehicle_number = models.CharField(max_length=20, blank=True)
    items_carried = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=VISITOR_STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='approved_visitor_passes')
    approval_remarks = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    actual_out_time = models.TimeField(null=True, blank=True)
    visitor_photo = models.ImageField(upload_to='visitor_photos/', null=True, blank=True)
    created_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='created_visitor_passes')
    approval_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pass_number:
            from accounts.models import SystemSetting
            s = SystemSetting.get()
            self.pass_number = f'{s.vgp_prefix}-{s.vgp_next_number:05d}'
            s.vgp_next_number += 1
            s.save(update_fields=['vgp_next_number'])
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.pass_number, self.visitor_name)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Visitor Gate Pass'
