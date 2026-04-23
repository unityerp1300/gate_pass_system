from django import forms
from .models import Grievance, GrievanceComment


class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = [
            'category', 'priority', 'subject', 'description', 'attachment',
            'notify_management', 'notify_president', 'notify_hod', 'notify_hr',
        ]
        widgets = {
            'subject':     forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category':    forms.Select(attrs={'class': 'form-select'}),
            'priority':    forms.Select(attrs={'class': 'form-select'}),
            'attachment':  forms.FileInput(attrs={'class': 'form-control'}),
        }


class GrievanceUpdateForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['status', 'assigned_to', 'resolution_note']
        widgets = {
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'assigned_to':     forms.Select(attrs={'class': 'form-select'}),
            'resolution_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class GrievanceCommentForm(forms.ModelForm):
    class Meta:
        model = GrievanceComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment…'}),
        }
