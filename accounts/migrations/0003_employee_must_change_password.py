from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_update_department_role_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='must_change_password',
            field=models.BooleanField(default=True),
        ),
    ]
