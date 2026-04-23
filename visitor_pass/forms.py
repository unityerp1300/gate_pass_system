from django import forms
from .models import VisitorGatePass
from accounts.models import Employee
from .models import MATERIAL_CATEGORY_CHOICES


class VisitorGatePassForm(forms.ModelForm):
    now_visit_date = forms.BooleanField(required=False, label='Today')
    now_in_time    = forms.BooleanField(required=False, label='Now')
    now_out_time   = forms.BooleanField(required=False, label='Now')

    class Meta:
        model = VisitorGatePass
        fields = [
            'visitor_name', 'visitor_company', 'visitor_city', 'visitor_phone', 'visitor_email',
            'id_type', 'id_number', 'no_of_visitors', 'visit_purpose', 'visit_detail',
            'material', 'material_category', 'access_card_no',
            'person_to_meet', 'visit_date', 'in_time', 'expected_out_time',
            'vehicle_number', 'items_carried',
        ]
        labels = {'visitor_city': 'City'}
        widgets = {
            'visitor_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_company':   forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_city':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'visitor_phone':     forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_email':     forms.EmailInput(attrs={'class': 'form-control'}),
            'id_type':           forms.Select(attrs={'class': 'form-select'}),
            'id_number':         forms.TextInput(attrs={'class': 'form-control'}),
            'no_of_visitors':    forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'visit_purpose':     forms.Select(attrs={'class': 'form-select'}),
            'visit_detail':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'material':          forms.TextInput(attrs={'class': 'form-control'}),
            # Rendered as radio buttons in template (Returnable / Non-Returnable)
            'material_category': forms.RadioSelect(),
            'access_card_no':    forms.TextInput(attrs={'class': 'form-control'}),
            'person_to_meet':    forms.Select(attrs={'class': 'form-select'}),
            'visit_date':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_visit_date'}),
            'in_time':           forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_in_time'}),
            'expected_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_expected_out_time'}),
            'vehicle_number':    forms.TextInput(attrs={'class': 'form-control'}),
            'items_carried':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person_to_meet'].queryset = Employee.objects.filter(is_active=True)
        # Remove the blank choice so only Returnable/Non-Returnable show.
        # Keep required=False because model allows blank.
        self.fields['material_category'].required = False
        self.fields['material_category'].choices = list(MATERIAL_CATEGORY_CHOICES)


class VisitorApprovalForm(forms.Form):
    action = forms.ChoiceField(choices=[('approved', 'Approve'), ('rejected', 'Reject')],
                               widget=forms.Select(attrs={'class': 'form-select'}))
    remarks = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


class CheckoutForm(forms.Form):
    now_checkout = forms.BooleanField(required=False, label='Use current time')
    actual_out_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_actual_out_time'})
    )

    def clean(self):
        from django.utils import timezone
        cleaned = super().clean()
        if cleaned.get('now_checkout'):
            cleaned['actual_out_time'] = timezone.localtime(timezone.now()).time()
        if not cleaned.get('actual_out_time'):
            raise forms.ValidationError('Please enter checkout time or check "Use current time".')
        return cleaned


class PhotoCaptureForm(forms.ModelForm):
    class Meta:
        model = VisitorGatePass
        fields = ['visitor_photo']
        widgets = {
            'visitor_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
