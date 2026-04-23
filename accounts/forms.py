from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee, FULL_ACCESS_ROLES, RolePermissionTemplate

OTP_DEFAULT = '123456'

PERM_FIELDS = RolePermissionTemplate.PERM_FIELDS


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class EmployeeForm(forms.ModelForm):
    additional_departments = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
        label='Additional Departments'
    )
    additional_roles = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
        label='Additional Roles'
    )
    password_plain = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep current'}),
        label='Password (Admin View)'
    )

    class Meta:
        model = Employee
        fields = [
            'employee_name', 'employee_code', 'department', 'additional_departments', 'designation', 'role', 'additional_roles',
            'reporting_person', 'joining_date', 'email', 'username', 'password_plain',
            'is_active',
        ] + PERM_FIELDS + ['perm_hd_raise', 'perm_mgp_request', 'perm_grv_view', 'perm_grv_write', 'perm_grv_manage']
        widgets = {
            'employee_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'employee_code':    forms.TextInput(attrs={'class': 'form-control'}),
            'department':       forms.Select(attrs={'class': 'form-select'}),
            'designation':      forms.TextInput(attrs={'class': 'form-control'}),
            'role':             forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}),
            'reporting_person': forms.Select(attrs={'class': 'form-select'}),
            'joining_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email':            forms.EmailInput(attrs={'class': 'form-control'}),
            'username':         forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_additional_departments([
            value for value in self.cleaned_data.get('additional_departments', [])
            if value != user.department
        ])
        user.set_additional_roles([
            value for value in self.cleaned_data.get('additional_roles', [])
            if value != user.role
        ])
        plain = self.cleaned_data.get('password_plain', '').strip()
        if not user.pk:
            # New employee — set OTP default
            user.set_password(OTP_DEFAULT)
            user.password_plain = OTP_DEFAULT
            user.must_change_password = True
        elif plain:
            # Admin explicitly set a new password
            user.set_password(plain)
            user.password_plain = plain
            # Do NOT force must_change_password — admin is setting it intentionally
        # If blank on edit — leave password and must_change_password untouched
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import DEPARTMENT_CHOICES, ROLE_CHOICES
        self.fields['additional_departments'].choices = DEPARTMENT_CHOICES
        self.fields['additional_roles'].choices = ROLE_CHOICES
        if self.instance and self.instance.pk:
            self.initial.setdefault('additional_departments', self.instance.get_additional_departments())
            self.initial.setdefault('additional_roles', self.instance.get_additional_roles())


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        if p1 and p1 == OTP_DEFAULT:
            raise forms.ValidationError('New password cannot be the same as the one-time password.')
        return cleaned


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        label='Registered Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your registered email'})
    )


class ForgotPasswordSetForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
