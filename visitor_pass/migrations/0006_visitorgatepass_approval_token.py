import uuid
from django.db import migrations, models


def populate_tokens(apps, schema_editor):
    VGP = apps.get_model('visitor_pass', 'VisitorGatePass')
    for obj in VGP.objects.all():
        obj.approval_token = uuid.uuid4()
        obj.save(update_fields=['approval_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_pass', '0005_visitorgatepass_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorgatepass',
            name='approval_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(populate_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='visitorgatepass',
            name='approval_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
