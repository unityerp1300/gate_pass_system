from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_employee_multi_department_role_and_duplicate_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='grv_prefix',
            field=models.CharField(default='GRV', max_length=10, verbose_name='Grievance Prefix'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='grv_next_number',
            field=models.PositiveIntegerField(default=1, verbose_name='GRV Next Number'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_grv_view',
            field=models.BooleanField(default=True, verbose_name='Grievance View'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_grv_write',
            field=models.BooleanField(default=True, verbose_name='Grievance Raise'),
        ),
        migrations.AddField(
            model_name='employee',
            name='perm_grv_manage',
            field=models.BooleanField(default=False, verbose_name='Grievance Manage'),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_grv_view',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_grv_write',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rolepermissiontemplate',
            name='perm_grv_manage',
            field=models.BooleanField(default=False),
        ),
    ]
