from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0020_remove_notificationpermission_unique_notification_permission_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemsetting",
            name="notif_hd_email",
            field=models.BooleanField(default=True, verbose_name="HD Email Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_hd_popup",
            field=models.BooleanField(default=True, verbose_name="HD Popup Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_igp_email",
            field=models.BooleanField(default=True, verbose_name="IGP Email Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_igp_popup",
            field=models.BooleanField(default=True, verbose_name="IGP Popup Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_mgp_email",
            field=models.BooleanField(default=True, verbose_name="MGP Email Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_mgp_popup",
            field=models.BooleanField(default=True, verbose_name="MGP Popup Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_vgp_email",
            field=models.BooleanField(default=True, verbose_name="VGP Email Notifications"),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="notif_vgp_popup",
            field=models.BooleanField(default=True, verbose_name="VGP Popup Notifications"),
        ),
    ]
