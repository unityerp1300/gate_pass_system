from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auditlog'),
    ]

    operations = [
        # Step 1: Remove old boolean fields (they exist in DB from 0001_initial)
        migrations.RemoveField(model_name='employee', name='can_access_dashboard'),
        migrations.RemoveField(model_name='employee', name='can_access_accounts'),
        migrations.RemoveField(model_name='employee', name='can_access_internal_pass'),
        migrations.RemoveField(model_name='employee', name='can_access_visitor_pass'),
        migrations.RemoveField(model_name='employee', name='can_approve_internal_pass'),
        migrations.RemoveField(model_name='employee', name='can_approve_visitor_pass'),

        # Step 2: Add new granular permission fields
        migrations.AddField(model_name='employee', name='perm_dashboard_view',  field=models.BooleanField(default=True,  verbose_name='Dashboard View')),
        migrations.AddField(model_name='employee', name='perm_accounts_view',   field=models.BooleanField(default=False, verbose_name='Accounts View')),
        migrations.AddField(model_name='employee', name='perm_accounts_write',  field=models.BooleanField(default=False, verbose_name='Accounts Write')),
        migrations.AddField(model_name='employee', name='perm_accounts_delete', field=models.BooleanField(default=False, verbose_name='Accounts Delete')),
        migrations.AddField(model_name='employee', name='perm_accounts_export', field=models.BooleanField(default=False, verbose_name='Accounts Export')),
        migrations.AddField(model_name='employee', name='perm_igp_view',        field=models.BooleanField(default=True,  verbose_name='IGP View')),
        migrations.AddField(model_name='employee', name='perm_igp_write',       field=models.BooleanField(default=True,  verbose_name='IGP Write')),
        migrations.AddField(model_name='employee', name='perm_igp_delete',      field=models.BooleanField(default=False, verbose_name='IGP Delete')),
        migrations.AddField(model_name='employee', name='perm_igp_approve',     field=models.BooleanField(default=False, verbose_name='IGP Approve/Reject')),
        migrations.AddField(model_name='employee', name='perm_igp_bypass',      field=models.BooleanField(default=False, verbose_name='IGP Bypass Approval')),
        migrations.AddField(model_name='employee', name='perm_igp_export',      field=models.BooleanField(default=False, verbose_name='IGP Export Reports')),
        migrations.AddField(model_name='employee', name='perm_vgp_view',        field=models.BooleanField(default=True,  verbose_name='VGP View')),
        migrations.AddField(model_name='employee', name='perm_vgp_write',       field=models.BooleanField(default=True,  verbose_name='VGP Write')),
        migrations.AddField(model_name='employee', name='perm_vgp_delete',      field=models.BooleanField(default=False, verbose_name='VGP Delete')),
        migrations.AddField(model_name='employee', name='perm_vgp_approve',     field=models.BooleanField(default=False, verbose_name='VGP Approve/Reject')),
        migrations.AddField(model_name='employee', name='perm_vgp_bypass',      field=models.BooleanField(default=False, verbose_name='VGP Bypass Approval')),
        migrations.AddField(model_name='employee', name='perm_vgp_export',      field=models.BooleanField(default=False, verbose_name='VGP Export Reports')),

        # Step 3: Create RolePermissionTemplate model
        migrations.CreateModel(
            name='RolePermissionTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=30, unique=True, choices=[
                    ('administrator', 'Administrator'), ('management', 'Management'),
                    ('president_plant_head', 'President-Plant Head'), ('department_hod', 'Department HOD'),
                    ('hr', 'HR'), ('security', 'Security'), ('employee', 'Employee'),
                ])),
                ('perm_dashboard_view',  models.BooleanField(default=True)),
                ('perm_accounts_view',   models.BooleanField(default=False)),
                ('perm_accounts_write',  models.BooleanField(default=False)),
                ('perm_accounts_delete', models.BooleanField(default=False)),
                ('perm_accounts_export', models.BooleanField(default=False)),
                ('perm_igp_view',        models.BooleanField(default=True)),
                ('perm_igp_write',       models.BooleanField(default=True)),
                ('perm_igp_delete',      models.BooleanField(default=False)),
                ('perm_igp_approve',     models.BooleanField(default=False)),
                ('perm_igp_bypass',      models.BooleanField(default=False)),
                ('perm_igp_export',      models.BooleanField(default=False)),
                ('perm_vgp_view',        models.BooleanField(default=True)),
                ('perm_vgp_write',       models.BooleanField(default=True)),
                ('perm_vgp_delete',      models.BooleanField(default=False)),
                ('perm_vgp_approve',     models.BooleanField(default=False)),
                ('perm_vgp_bypass',      models.BooleanField(default=False)),
                ('perm_vgp_export',      models.BooleanField(default=False)),
            ],
            options={'verbose_name': 'Role Permission Template'},
        ),
    ]
