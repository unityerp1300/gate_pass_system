from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_systemsetting_session_timeout_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='perm_reports_mgp',
            field=models.BooleanField(default=False, verbose_name='MGP Reports View'),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_reports_mgp',
            field=models.BooleanField(default=False),
        ),
    ]

