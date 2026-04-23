from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_reports_mgp_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='welcome_seen_version',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='welcome_enabled',
            field=models.BooleanField(default=False, verbose_name='Enable Inauguration Page'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='welcome_message_management',
            field=models.TextField(blank=True, default='A brief message from the entire Management Team.'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='welcome_message_president',
            field=models.TextField(blank=True, default='A brief message from the President-Plant Head.'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='welcome_title',
            field=models.CharField(blank=True, default='Welcome to the ERP System', max_length=120),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='welcome_version',
            field=models.PositiveIntegerField(default=1, verbose_name='Inauguration Version'),
        ),
    ]

