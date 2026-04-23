from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0021_systemsetting_workflow_notification_channels"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField(blank=True)),
                ("channel", models.CharField(choices=[("igp", "IGP"), ("vgp", "VGP"), ("mgp", "MGP"), ("hd", "Help Desk"), ("system", "System")], default="system", max_length=20)),
                ("status", models.CharField(default="sent", max_length=20)),
                ("related_id", models.CharField(blank=True, max_length=50)),
                ("related_module", models.CharField(blank=True, max_length=20)),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Email Log",
                "ordering": ["-created_at"],
            },
        ),
    ]
