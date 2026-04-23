from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_employee_session_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('action', models.CharField(max_length=30, choices=[
                    ('login','Login'),('logout','Logout'),('login_failed','Login Failed'),
                    ('otp_verified','OTP Verified'),('session_timeout','Session Timeout'),
                    ('duplicate_kick','Duplicate Session Kicked'),
                    ('igp_create','IGP Created'),('igp_approve','IGP Approved'),
                    ('igp_reject','IGP Rejected'),('igp_return','IGP Returned'),
                    ('vgp_create','VGP Created'),('vgp_approve','VGP Approved'),
                    ('vgp_reject','VGP Rejected'),('vgp_checkout','VGP Checked Out'),
                    ('employee_create','Employee Created'),('employee_edit','Employee Edited'),
                    ('employee_delete','Employee Deleted'),('settings_change','Settings Changed'),
                    ('password_reset','Password Reset'),('page_view','Page View'),
                ])),
                ('module', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField(blank=True)),
                ('extra', models.JSONField(blank=True, default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='audit_logs',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['-timestamp'], 'verbose_name': 'Audit Log'},
        ),
    ]
