from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_grievance_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='perm_hd_raise',
            field=models.BooleanField(default=True, verbose_name='HD Raise Ticket'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_mgp_request',
            field=models.BooleanField(default=True, verbose_name='MGP Request Raise'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='igp_print_fields',
            field=models.TextField(blank=True, default='', verbose_name='IGP Print Fields Config (JSON)'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='vgp_print_fields',
            field=models.TextField(blank=True, default='', verbose_name='VGP Print Fields Config (JSON)'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='mgp_print_fields',
            field=models.TextField(blank=True, default='', verbose_name='MGP Print Fields Config (JSON)'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='workflow_email_recipients',
            field=models.TextField(blank=True, default='', verbose_name='Workflow Email Recipients (JSON)'),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_hd_raise',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_mgp_request',
            field=models.BooleanField(default=True),
        ),
    ]
