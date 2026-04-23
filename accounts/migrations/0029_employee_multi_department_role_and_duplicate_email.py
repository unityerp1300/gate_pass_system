from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_normalize_mgp_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='additional_departments',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='employee',
            name='additional_roles',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
