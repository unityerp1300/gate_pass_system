from django import forms
from .models import InternalGatePass


class InternalGatePassForm(forms.ModelForm):
    now_out_date = forms.BooleanField(required=False, label='Today')
    now_out_time = forms.BooleanField(required=False, label='Now')
    on_leave     = forms.BooleanField(required=False, label='On Leave (no return time needed)')

    class Meta:
        model = InternalGatePass
        fields = ['purpose', 'purpose_detail', 'destination', 'out_date', 'out_time',
                  'expected_return_time', 'transport_mode', 'vehicle_number']
        labels = {'destination': 'City'}
        widgets = {
            'purpose':              forms.Select(attrs={'class': 'form-select'}),
            'purpose_detail':       forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'destination':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'out_date':             forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_out_date'}),
            'out_time':             forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_out_time'}),
            'expected_return_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_expected_return_time'}),
            'transport_mode':       forms.Select(attrs={'class': 'form-select'}),
            'vehicle_number':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'If applicable'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expected_return_time'].required = False


class ApprovalForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('approved', 'Approve'), ('rejected', 'Reject')],
        widget=forms.RadioSelect()
    )
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


class ReturnForm(forms.Form):
    now_return = forms.BooleanField(required=False, label='Use current time')
    actual_return_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_actual_return_time'})
    )

    def clean(self):
        from django.utils import timezone
        cleaned = super().clean()
        if cleaned.get('now_return'):
            cleaned['actual_return_time'] = timezone.localtime(timezone.now()).time()
        if not cleaned.get('actual_return_time'):
            raise forms.ValidationError('Please enter return time or check "Use current time".')
        return cleaned
