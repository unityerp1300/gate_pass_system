from django import forms
from .models import MaterialGatePass, MaterialItem, MaterialRequest, MaterialRequestItem, GST_TYPE_CHOICES, GST_RATE_CHOICES
from accounts.models import DEPARTMENT_CHOICES


class MaterialGatePassForm(forms.ModelForm):
    class Meta:
        model = MaterialGatePass
        fields = [
            'department', 'direction', 'is_returnable', 'copy_type',
            'vehicle_number', 'transporter_name', 'lr_number', 'transport_mode',
            'pass_date', 'pass_time', 'expected_return_date',
            'consignor_name', 'consignor_address', 'consignor_office_address', 'consignor_contact',
            'consignor_state', 'consignor_state_code', 'consignor_pan', 'consignor_gstin',
            'party_name', 'party_address', 'city',
            'party_contact_person', 'party_contact_number',
            'party_state', 'party_pan', 'party_gstin',
            'gst_type', 'gst_rate', 'rounding_off',
            'bank_name', 'bank_account_number', 'bank_ifsc',
            'reason', 'remarks',
        ]
        widgets = {
            'department':           forms.Select(attrs={'class': 'form-select'}),
            'direction':            forms.Select(attrs={'class': 'form-select'}),
            'is_returnable':        forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'id_is_returnable'}),
            'copy_type':            forms.Select(attrs={'class': 'form-select'}),
            'vehicle_number':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MP09AB1234 (optional)'}),
            'transporter_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transporter name (optional)'}),
            'lr_number':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LR / GR number (optional)'}),
            'transport_mode':       forms.Select(attrs={'class': 'form-select'}),
            'pass_date':            forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pass_time':            forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'expected_return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_expected_return_date'}),
            'consignor_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'consignor_address':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'consignor_office_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'consignor_contact':    forms.TextInput(attrs={'class': 'form-control'}),
            'consignor_state':      forms.TextInput(attrs={'class': 'form-control'}),
            'consignor_state_code': forms.TextInput(attrs={'class': 'form-control'}),
            'consignor_pan':        forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'consignor_gstin':      forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'party_name':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Consignee / Party name'}),
            'party_address':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full address'}),
            'city':                 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'party_contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'party_contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91-XXXXXXXXXX'}),
            'party_state':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'party_pan':            forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'party_gstin':          forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'gst_type':             forms.Select(attrs={'class': 'form-select', 'id': 'id_gst_type'}),
            'gst_rate':             forms.Select(attrs={'class': 'form-select', 'id': 'id_gst_rate'}),
            'rounding_off':         forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bank_name':            forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'bank_ifsc':            forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'reason':               forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Reason for dispatch'}),
            'remarks':              forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vehicle details — non-mandatory
        for f in ['vehicle_number', 'transporter_name', 'lr_number']:
            self.fields[f].required = False
        # GST/rate fields — non-mandatory
        for f in ['gst_rate', 'rounding_off', 'bank_name', 'bank_account_number', 'bank_ifsc']:
            self.fields[f].required = False


class MaterialItemForm(forms.ModelForm):
    class Meta:
        model = MaterialItem
        fields = ['description', 'hsn_code', 'quantity', 'unit', 'rate', 'serial_number']
        widgets = {
            'description':   forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Particulars / description'}),
            'hsn_code':      forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'HSN'}),
            'quantity':      forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01', 'min': '0'}),
            'unit':          forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nos/Kg/Ltr'}),
            'rate':          forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01', 'min': '0'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Optional'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # rate is non-mandatory
        self.fields['rate'].required = False
        self.fields['rate'].initial = 0


MaterialItemFormSet = forms.inlineformset_factory(
    MaterialGatePass, MaterialItem,
    form=MaterialItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)


class MaterialRequestForm(forms.ModelForm):
    class Meta:
        model = MaterialRequest
        fields = ['department', 'is_returnable', 'request_date', 'expected_date', 'reason', 'remarks']
        widgets = {
            'department':    forms.Select(attrs={'class': 'form-select'}),
            'is_returnable': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_returnable'}),
            'request_date':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason / purpose for this request'}),
            'remarks':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class MaterialRequestItemForm(forms.ModelForm):
    class Meta:
        model = MaterialRequestItem
        fields = ['description', 'hsn_code', 'quantity', 'unit', 'remarks']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Item description'}),
            'hsn_code':    forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'HSN'}),
            'quantity':    forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01', 'min': '0'}),
            'unit':        forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nos/Kg/Ltr'}),
            'remarks':     forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Optional'}),
        }


MaterialRequestItemFormSet = forms.inlineformset_factory(
    MaterialRequest, MaterialRequestItem,
    form=MaterialRequestItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)


class HodReviewForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('hod_approved', 'Approve'), ('hod_rejected', 'Reject')],
        widget=forms.RadioSelect()
    )
    hod_remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'HOD remarks...'})
    )


class StoreReviewForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('store_approved', 'Approve'), ('store_rejected', 'Reject')],
        widget=forms.RadioSelect()
    )
    review_remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Store HOD remarks...'})
    )


class ApprovalForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('approved', 'Approve'), ('rejected', 'Reject')],
        widget=forms.RadioSelect()
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional remarks...'})
    )


class ReturnForm(forms.Form):
    actual_return_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
