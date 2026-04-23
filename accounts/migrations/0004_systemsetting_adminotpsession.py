from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_employee_must_change_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('igp_prefix', models.CharField(default='IGP', max_length=10, verbose_name='Internal Pass Prefix')),
                ('igp_next_number', models.PositiveIntegerField(default=1, verbose_name='IGP Next Number')),
                ('vgp_prefix', models.CharField(default='VGP', max_length=10, verbose_name='Visitor Pass Prefix')),
                ('vgp_next_number', models.PositiveIntegerField(default=1, verbose_name='VGP Next Number')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'System Setting'},
        ),
        migrations.CreateModel(
            name='AdminOTPSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('employee', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='otp_session',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
    ]
