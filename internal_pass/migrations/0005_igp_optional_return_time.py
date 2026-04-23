from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_pass', '0004_alter_internalgatepass_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalgatepass',
            name='expected_return_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
