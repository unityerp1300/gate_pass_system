from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visitor_pass', '0004_alter_visitorgatepass_visitor_location'),
        ('accounts', '0013_material_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorgatepass',
            name='created_by',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='created_visitor_passes',
                to='accounts.employee',
            ),
        ),
    ]
