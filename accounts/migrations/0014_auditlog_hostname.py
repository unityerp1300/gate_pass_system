from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_material_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='hostname',
            field=models.CharField(blank=True, max_length=200, verbose_name='Desktop/Hostname'),
        ),
    ]
