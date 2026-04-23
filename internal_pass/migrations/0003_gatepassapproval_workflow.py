import secrets
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internal_pass', '0002_internalgatepass_approval_token'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='internalgatepass',
            name='current_stage',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='internalgatepass',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'), ('in_progress', 'In Progress'),
                    ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned'),
                ],
                default='pending', max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='GatePassApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.PositiveSmallIntegerField()),
                ('stage_label', models.CharField(max_length=100)),
                ('approver_role', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('remarks', models.TextField(blank=True)),
                ('token', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('acted_at', models.DateTimeField(blank=True, null=True)),
                ('gate_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='internal_pass.internalgatepass')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stage_approvals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['stage'],
                'unique_together': {('gate_pass', 'stage')},
            },
        ),
    ]
