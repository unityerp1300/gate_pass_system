from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_granular_permissions'),
    ]

    operations = [
        migrations.AddField(model_name='employee', name='perm_helpdesk_view',   field=models.BooleanField(default=True,  verbose_name='Help Desk View')),
        migrations.AddField(model_name='employee', name='perm_helpdesk_write',  field=models.BooleanField(default=True,  verbose_name='Help Desk Raise Ticket')),
        migrations.AddField(model_name='employee', name='perm_helpdesk_manage', field=models.BooleanField(default=False, verbose_name='Help Desk Manage (IT)')),
        migrations.AddField(model_name='rolepermissiontemplate', name='perm_helpdesk_view',   field=models.BooleanField(default=True)),
        migrations.AddField(model_name='rolepermissiontemplate', name='perm_helpdesk_write',  field=models.BooleanField(default=True)),
        migrations.AddField(model_name='rolepermissiontemplate', name='perm_helpdesk_manage', field=models.BooleanField(default=False)),
    ]
