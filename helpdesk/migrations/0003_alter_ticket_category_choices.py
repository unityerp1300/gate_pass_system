from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0002_ticket_doc_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(
                choices=[
                    ('hardware', 'Hardware Issue'),
                    ('software', 'Software Issue'),
                    ('network', 'Network / Internet'),
                    ('email', 'Email / Outlook'),
                    ('printer', 'Printer / Scanner'),
                    ('access', 'Access / Login'),
                    ('cctv', 'CCTV'),
                    ('other', 'Other'),
                ],
                max_length=30,
            ),
        ),
    ]

