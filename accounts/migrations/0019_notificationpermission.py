# Generated migration for NotificationPermission model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(choices=[('role', 'By Role'), ('employee', 'By Employee'), ('department', 'By Department')], help_text='Scope of this permission', max_length=20)),
                ('role', models.CharField(blank=True, help_text='Role (if scope=role)', max_length=50)),
                ('department', models.CharField(blank=True, choices=[('Management', 'Management'), ('Whole Plant', 'Whole Plant'), ('Administrator/ERP', 'Administrator/ERP'), ('Security', 'Security'), ('HR & Admin', 'HR & Admin'), ('HSEF', 'HSEF'), ('Mechanical (Crushing & Pyro)', 'Mechanical (Crushing & Pyro)'), ('Mechanical (Packing & Utility & Grinding)', 'Mechanical (Packing & Utility & Grinding)'), ('Electrical', 'Electrical'), ('Instrument', 'Instrument'), ('Process & Production', 'Process & Production'), ('QC', 'QC'), ('Civil', 'Civil'), ('IT', 'IT'), ('Purchase', 'Purchase'), ('Logistics', 'Logistics'), ('Store', 'Store'), ('Automobile', 'Automobile'), ('Account', 'Account'), ('Sales Account', 'Sales Account'), ('Sales', 'Sales'), ('Marketing', 'Marketing')], help_text='Department (if scope=department)', max_length=100)),
                ('notification_type', models.CharField(choices=[('igp_approved', 'IGP Approved'), ('igp_rejected', 'IGP Rejected'), ('vgp_approved', 'VGP Approved'), ('vgp_rejected', 'VGP Rejected'), ('mgp_approved', 'MGP Approved'), ('mgp_rejected', 'MGP Rejected'), ('hd_resolved', 'Ticket Resolved'), ('hd_assigned', 'Ticket Assigned'), ('all', 'All Notifications')], help_text='Which notification type is allowed', max_length=30)),
                ('can_receive', models.BooleanField(default=True, help_text='Can this group receive this notification type?')),
                ('can_view_own', models.BooleanField(default=True, help_text='Can view their own notifications?')),
                ('can_view_department', models.BooleanField(default=False, help_text='Can view department notifications?')),
                ('can_view_all', models.BooleanField(default=False, help_text='Can view all notifications?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(blank=True, help_text='Employee (if scope=employee)', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employee')),
            ],
            options={
                'verbose_name': 'Notification Permission',
                'verbose_name_plural': 'Notification Permissions',
            },
        ),
        migrations.AddConstraint(
            model_name='notificationpermission',
            constraint=models.UniqueConstraint(fields=('scope', 'role', 'employee', 'department', 'notification_type'), name='unique_notification_permission'),
        ),
    ]
