# Generated migration for Notification model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_inauguration_page_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('igp_approved', 'IGP Approved'), ('igp_rejected', 'IGP Rejected'), ('vgp_approved', 'VGP Approved'), ('vgp_rejected', 'VGP Rejected'), ('mgp_approved', 'MGP Approved'), ('mgp_rejected', 'MGP Rejected'), ('hd_resolved', 'Ticket Resolved'), ('hd_assigned', 'Ticket Assigned')], max_length=30)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('related_id', models.CharField(blank=True, max_length=50)),
                ('related_module', models.CharField(blank=True, max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='accounts.employee')),
            ],
            options={
                'verbose_name': 'Notification',
                'ordering': ['-created_at'],
            },
        ),
    ]
