import secrets
from django.db import models
from accounts.models import Employee, DEPARTMENT_CHOICES

STATUS_CHOICES = [
    ('pending',  'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('returned', 'Returned'),
]

REQUEST_STATUS_CHOICES = [
    ('draft',         'Draft'),
    ('submitted',     'Submitted — Pending HOD Approval'),
    ('hod_approved',  'HOD Approved — Pending Store HOD'),
    ('hod_rejected',  'Rejected by HOD'),
    ('store_approved','Approved by Store HOD'),
    ('store_rejected','Rejected by Store HOD'),
    ('converted',     'Converted to Gate Pass'),
]

DIRECTION_CHOICES = [
    ('outgoing', 'Outgoing (Out of Factory)'),
    ('incoming', 'Incoming (Into Factory)'),
]

TRANSPORT_MODE_CHOICES = [
    ('road',    'Road'),
    ('rail',    'Rail'),
    ('air',     'Air'),
    ('courier', 'Courier'),
    ('hand',    'By Hand'),
    ('other',   'Other'),
]

COPY_CHOICES = [
    ('original',    'Original for Buyer'),
    ('duplicate',   'Duplicate for Transporter'),
    ('triplicate',  'Triplicate for Supplier'),
]

GST_TYPE_CHOICES = [
    ('cgst_sgst', 'CGST + SGST (Intra-State)'),
    ('igst',      'IGST (Inter-State)'),
    ('none',      'Exempt / Nil Rated'),
]

# Official GST rate slabs as per Government of India
GST_RATE_CHOICES = [
    ('0.00',  '0% — Exempt / Nil'),
    ('0.10',  '0.1% — Special (e.g. certain food items)'),
    ('0.25',  '0.25% — Rough diamonds'),
    ('1.50',  '1.5% — Cut & polished diamonds / precious stones'),
    ('3.00',  '3% — Gold, Silver, Jewellery'),
    ('5.00',  '5% — Essential goods (food, transport, etc.)'),
    ('12.00', '12% — Standard goods (processed food, etc.)'),
    ('18.00', '18% — Standard goods (most goods & services)'),
    ('28.00', '28% — Luxury / demerit goods (cement, cars, etc.)'),
]

# Company constants — edit once here
COMPANY_NAME        = 'PMC CEMENT LTD.'
COMPANY_FACTORY_ADDR = 'Village Nandni, Tehsil Sihora, Dist. Jabalpur (M.P.) - 483225'
COMPANY_OFFICE_ADDR  = 'Plot No. 12, Industrial Area, Jabalpur (M.P.) - 482001'
COMPANY_GSTIN        = '23AABCP1234A1Z5'
COMPANY_PAN          = 'AABCP1234A'
COMPANY_STATE        = 'Madhya Pradesh'
COMPANY_STATE_CODE   = '23'
COMPANY_BANK_NAME    = 'State Bank of India'
COMPANY_BANK_ACCOUNT = '1234567890'
COMPANY_BANK_IFSC    = 'SBIN0001234'
COMPANY_CONTACT      = '+91-761-XXXXXXX'


class MaterialRequest(models.Model):
    request_number   = models.CharField(max_length=20, unique=True, editable=False)
    employee         = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='material_requests')
    department       = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    is_returnable    = models.BooleanField(default=False, verbose_name='Returnable Material')
    request_date     = models.DateField()
    expected_date    = models.DateField(null=True, blank=True, verbose_name='Required By Date')
    reason           = models.TextField(verbose_name='Reason / Purpose')
    remarks          = models.TextField(blank=True, default='')
    status           = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='draft')
    # ── Stage 1: Dept HOD ─────────────────────────────────────────────────
    hod_by           = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='hod_approved_requests')
    hod_at           = models.DateTimeField(null=True, blank=True)
    hod_remarks      = models.TextField(blank=True, default='')
    hod_token        = models.CharField(max_length=64, blank=True, null=True, unique=True)
    # ── Stage 2: Store HOD ────────────────────────────────────────────────
    reviewed_by      = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_requests')
    reviewed_at      = models.DateTimeField(null=True, blank=True)
    review_remarks   = models.TextField(blank=True, default='')
    store_hod_token  = models.CharField(max_length=64, blank=True, null=True, unique=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.request_number:
            from accounts.models import SystemSetting
            s = SystemSetting.get()
            prefix = getattr(s, 'mr_prefix', 'MR')
            next_no = getattr(s, 'mr_next_number', 1)
            self.request_number = f'{prefix}-{next_no:05d}'
            s.mr_next_number = next_no + 1
            s.save(update_fields=['mr_next_number'])
        if not self.hod_token:
            self.hod_token = secrets.token_urlsafe(32)
        if not self.store_hod_token:
            self.store_hod_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_number} - {self.employee.employee_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Material Gate Pass Request'


class MaterialRequestItem(models.Model):
    request     = models.ForeignKey(MaterialRequest, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300, verbose_name='Item Description')
    hsn_code    = models.CharField(max_length=20, blank=True, default='')
    quantity    = models.DecimalField(max_digits=10, decimal_places=2)
    unit        = models.CharField(max_length=30, default='')
    remarks     = models.CharField(max_length=300, blank=True, default='')

    def __str__(self):
        return f"{self.description} ({self.quantity} {self.unit})"

    class Meta:
        verbose_name = 'Material Gate Pass Request Item'


class MaterialGatePass(models.Model):
    pass_number          = models.CharField(max_length=20, unique=True, editable=False)
    employee             = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='material_passes')
    department           = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    request_ref          = models.ForeignKey('MaterialRequest', null=True, blank=True, on_delete=models.SET_NULL, related_name='gate_passes', verbose_name='Material Request')
    direction            = models.CharField(max_length=20, choices=DIRECTION_CHOICES, default='outgoing')
    is_returnable        = models.BooleanField(default=False, verbose_name='Returnable Material')
    copy_type            = models.CharField(max_length=20, choices=COPY_CHOICES, default='original', blank=True, verbose_name='Document Copy')

    # ── Dispatch / Transport ──────────────────────────────────────────────
    vehicle_number       = models.CharField(max_length=30, blank=True, default='')
    transporter_name     = models.CharField(max_length=200, blank=True, default='')
    lr_number            = models.CharField(max_length=100, blank=True, default='', verbose_name='LR No.')
    transport_mode       = models.CharField(max_length=20, choices=TRANSPORT_MODE_CHOICES, default='road')

    # ── Invoice / Pass Info ───────────────────────────────────────────────
    pass_date            = models.DateField()
    pass_time            = models.TimeField()
    expected_return_date = models.DateField(null=True, blank=True, verbose_name='Expected Return Date')
    reason               = models.TextField(blank=True, default='', verbose_name='Reason for Dispatch')
    remarks              = models.TextField(blank=True, default='')

    # ── Consignor (Sender — our company) ─────────────────────────────────
    consignor_name       = models.CharField(max_length=200, default=COMPANY_NAME)
    consignor_address    = models.TextField(default=COMPANY_FACTORY_ADDR)
    consignor_office_address = models.TextField(blank=True, default=COMPANY_OFFICE_ADDR, verbose_name='Office Address')
    consignor_contact    = models.CharField(max_length=50, blank=True, default='')
    consignor_state      = models.CharField(max_length=100, default=COMPANY_STATE)
    consignor_state_code = models.CharField(max_length=10, default=COMPANY_STATE_CODE)
    consignor_pan        = models.CharField(max_length=20, default=COMPANY_PAN)
    consignor_gstin      = models.CharField(max_length=20, default=COMPANY_GSTIN, verbose_name='Consignor GSTIN')

    # ── Consignee (Receiver — party) ─────────────────────────────────────
    party_name           = models.CharField(max_length=200, default='', verbose_name='Consignee / Party Name')
    party_address        = models.TextField(default='', verbose_name='Consignee Full Address')
    city                 = models.CharField(max_length=100, default='')
    party_contact_person = models.CharField(max_length=100, blank=True, default='')
    party_contact_number = models.CharField(max_length=20, blank=True, default='')
    party_state          = models.CharField(max_length=100, blank=True, default='')
    party_pan            = models.CharField(max_length=20, blank=True, default='', verbose_name='Consignee PAN')
    party_gstin          = models.CharField(max_length=20, blank=True, default='', verbose_name='Consignee GSTIN')

    # ── Bank ─────────────────────────────────────────────────────────────
    bank_name            = models.CharField(max_length=200, blank=True, default=COMPANY_BANK_NAME, verbose_name='Bank Name')
    bank_account_number  = models.CharField(max_length=50, blank=True, default=COMPANY_BANK_ACCOUNT, verbose_name='Account Number')
    bank_ifsc            = models.CharField(max_length=20, blank=True, default=COMPANY_BANK_IFSC, verbose_name='IFSC Code')

    # ── Tax ───────────────────────────────────────────────────────────────
    gst_type             = models.CharField(max_length=20, choices=GST_TYPE_CHOICES, default='cgst_sgst', verbose_name='GST Type')
    gst_rate             = models.CharField(max_length=6, choices=GST_RATE_CHOICES, default='18.00', verbose_name='GST Rate %')
    rounding_off         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Rounding Off')
    # legacy fields kept for old records
    cgst_rate            = models.DecimalField(max_digits=5, decimal_places=2, default=9.00, verbose_name='CGST %')
    sgst_rate            = models.DecimalField(max_digits=5, decimal_places=2, default=9.00, verbose_name='SGST %')

    # ── Approval ─────────────────────────────────────────────────────────
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approver             = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_material_passes')
    approval_remarks     = models.TextField(blank=True, default='')
    approved_at          = models.DateTimeField(null=True, blank=True)
    approval_token       = models.CharField(max_length=64, blank=True, null=True, unique=True)

    # ── Return ────────────────────────────────────────────────────────────
    actual_return_date   = models.DateField(null=True, blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pass_number:
            from accounts.models import SystemSetting
            s = SystemSetting.get()
            self.pass_number = f'{s.mgp_prefix}-{s.mgp_next_number:05d}'
            s.mgp_next_number += 1
            s.save(update_fields=['mgp_next_number'])
        if not self.approval_token:
            self.approval_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def get_type_label(self):
        return 'Returnable' if self.is_returnable else 'Non-Returnable'

    def _rate(self):
        return float(self.gst_rate)

    def get_subtotal(self):
        return round(sum(item.total_value for item in self.items.all()), 2)

    def get_cgst_amount(self):
        if self.gst_type != 'cgst_sgst':
            return 0.00
        return round(self.get_subtotal() * (self._rate() / 2) / 100, 2)

    def get_sgst_amount(self):
        if self.gst_type != 'cgst_sgst':
            return 0.00
        return round(self.get_subtotal() * (self._rate() / 2) / 100, 2)

    def get_igst_amount(self):
        if self.gst_type != 'igst':
            return 0.00
        return round(self.get_subtotal() * self._rate() / 100, 2)

    def get_tax_amount(self):
        if self.gst_type == 'cgst_sgst':
            return round(self.get_cgst_amount() + self.get_sgst_amount(), 2)
        return self.get_igst_amount()

    def get_grand_total(self):
        return round(self.get_subtotal() + self.get_tax_amount() + float(self.rounding_off), 2)

    def __str__(self):
        return f"{self.pass_number} - {self.employee.employee_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Material Gate Pass'


class MaterialItem(models.Model):
    gate_pass     = models.ForeignKey(MaterialGatePass, on_delete=models.CASCADE, related_name='items')
    description   = models.CharField(max_length=300, verbose_name='Particulars')
    hsn_code      = models.CharField(max_length=20, blank=True, default='', verbose_name='HSN Code')
    quantity      = models.DecimalField(max_digits=10, decimal_places=2)
    unit          = models.CharField(max_length=30, default='')
    rate          = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    serial_number = models.CharField(max_length=100, blank=True, default='')

    @property
    def total_value(self):
        return round(float(self.quantity) * float(self.rate), 2)

    def __str__(self):
        return f"{self.description} ({self.quantity} {self.unit})"

    class Meta:
        verbose_name = 'Material Item'


class MaterialAttachment(models.Model):
    gate_pass   = models.ForeignKey(MaterialGatePass, on_delete=models.CASCADE, related_name='attachments')
    file        = models.FileField(upload_to='mgp_attachments/')
    file_name   = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.file_name and self.file:
            self.file_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

    def is_image(self):
        ext = self.file_name.rsplit('.', 1)[-1].lower() if '.' in self.file_name else ''
        return ext in ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp')

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Material Attachment'
