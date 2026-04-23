from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auditlog_hostname'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='session_timeout_minutes',
            field=models.PositiveIntegerField(
                default=20,
                help_text='Inactivity timeout for all users (all roles).',
                verbose_name='Session Timeout (minutes)',
            ),
        ),
    ]

