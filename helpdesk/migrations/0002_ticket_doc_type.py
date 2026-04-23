from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='doc_type',
            field=models.CharField(
                choices=[
                    ('incident', 'Incident'),
                    ('service_request', 'Service Request'),
                    ('access_request', 'Access Request'),
                    ('change_request', 'Change Request'),
                    ('other', 'Other'),
                ],
                default='incident',
                max_length=30,
                verbose_name='DocType',
            ),
        ),
    ]

