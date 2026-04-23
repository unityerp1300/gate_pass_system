from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.CharField(
                max_length=100,
                choices=[
                    ('Management', 'Management'),
                    ('Whole Plant', 'Whole Plant'),
                    ('Administrator/ERP', 'Administrator/ERP'),
                    ('Security', 'Security'),
                    ('HR & Admin', 'HR & Admin'),
                    ('HSEF', 'HSEF'),
                    ('Mechanical (Crushing & Pyro)', 'Mechanical (Crushing & Pyro)'),
                    ('Mechanical (Packing & Utility & Grinding)', 'Mechanical (Packing & Utility & Grinding)'),
                    ('Electrical', 'Electrical'),
                    ('Instrument', 'Instrument'),
                    ('Process & Production', 'Process & Production'),
                    ('QC', 'QC'),
                    ('Civil', 'Civil'),
                    ('IT', 'IT'),
                    ('Purchase', 'Purchase'),
                    ('Logistics', 'Logistics'),
                    ('Store', 'Store'),
                    ('Automobile', 'Automobile'),
                    ('Account', 'Account'),
                    ('Sales Account', 'Sales Account'),
                    ('Sales', 'Sales'),
                    ('Marketing', 'Marketing'),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(
                max_length=30,
                default='employee',
                choices=[
                    ('administrator', 'Administrator'),
                    ('management', 'Management'),
                    ('president_plant_head', 'President-Plant Head'),
                    ('department_hod', 'Department HOD'),
                    ('hr', 'HR'),
                    ('security', 'Security'),
                    ('employee', 'Employee'),
                ],
            ),
        ),
    ]
