# Generated migration to support multiple workflow variants per pass type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_create_default_workflows'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationworkflow',
            name='creator_role',
            field=models.CharField(
                choices=[
                    ('employee', 'Employee'),
                    ('department_hod', 'Department HOD/HR'),
                    ('plant_head', 'Plant Head'),
                    ('security', 'Security'),
                    ('management', 'Management'),
                    ('any', 'Any Role (Default)'),
                ],
                default='any',
                help_text='Which role creates the pass - determines which workflow to use',
                max_length=50
            ),
        ),
        migrations.AlterField(
            model_name='notificationworkflow',
            name='pass_type',
            field=models.CharField(
                choices=[
                    ('igp', 'Internal Gate Pass (IGP)'),
                    ('vgp', 'Visitor Gate Pass (VGP)'),
                    ('mgp', 'Material Gate Pass (MGP)'),
                    ('helpdesk', 'IT Help Desk'),
                ],
                max_length=20
            ),
        ),
        migrations.AlterUniqueTogether(
            name='notificationworkflow',
            unique_together={('pass_type', 'creator_role')},
        ),
    ]
