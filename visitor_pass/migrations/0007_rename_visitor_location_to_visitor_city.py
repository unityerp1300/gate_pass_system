# Generated migration to rename visitor_location to visitor_city

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_pass', '0006_visitorgatepass_approval_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitorgatepass',
            old_name='visitor_location',
            new_name='visitor_city',
        ),
    ]
