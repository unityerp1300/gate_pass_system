from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_systemsetting_adminotpsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
