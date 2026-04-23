from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grievance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grievance_no', models.CharField(editable=False, max_length=20, unique=True)),
                ('category', models.CharField(choices=[('salary', 'Salary / Payroll'), ('harassment', 'Harassment / Misconduct'), ('workload', 'Workload / Work Conditions'), ('leave', 'Leave / Attendance'), ('safety', 'Safety / HSEF'), ('promotion', 'Promotion / Appraisal'), ('facilities', 'Facilities / Infrastructure'), ('other', 'Other')], max_length=30)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium', max_length=10)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='grievance_attachments/')),
                ('notify_management', models.BooleanField(default=True, verbose_name='Notify Management')),
                ('notify_president', models.BooleanField(default=True, verbose_name='Notify President / Plant Head')),
                ('notify_hod', models.BooleanField(default=True, verbose_name='Notify Department HOD')),
                ('notify_hr', models.BooleanField(default=True, verbose_name='Notify HR')),
                ('status', models.CharField(choices=[('open', 'Open'), ('under_review', 'Under Review'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=20)),
                ('resolution_note', models.TextField(blank=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grievances_assigned', to=settings.AUTH_USER_MODEL)),
                ('raised_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grievances_raised', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Grievance', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='GrievanceComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grievance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='grievance.grievance')),
            ],
            options={'ordering': ['created_at']},
        ),
    ]
