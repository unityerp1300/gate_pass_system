from django import forms
from django.db.models import Q
from .models import Ticket, TicketComment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['doc_type', 'title', 'category', 'priority', 'description']
        widgets = {
            'doc_type':    forms.Select(attrs={'class': 'form-select'}),
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of the issue'}),
            'category':    forms.Select(attrs={'class': 'form-select'}),
            'priority':    forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue in detail...'}),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'assigned_to', 'resolution_note']
        widgets = {
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'priority':        forms.Select(attrs={'class': 'form-select'}),
            'assigned_to':     forms.Select(attrs={'class': 'form-select'}),
            'resolution_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import Employee
        self.fields['assigned_to'].queryset = Employee.objects.filter(
            Q(is_active=True, department='IT') |
            Q(is_active=True, additional_departments__contains='|IT|')
        )
        self.fields['assigned_to'].empty_label = '— Unassigned —'


class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment', 'is_internal']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment or update...'}),
        }
