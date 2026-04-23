from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_pass', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalgatepass',
            name='approval_token',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
