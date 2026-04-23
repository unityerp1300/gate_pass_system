from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0022_emaillog"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationWorkflow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pass_type", models.CharField(
                    choices=[
                        ("igp", "Internal Gate Pass (IGP)"),
                        ("vgp", "Visitor Gate Pass (VGP)"),
                        ("mgp", "Material Gate Pass (MGP)"),
                        ("helpdesk", "IT Help Desk"),
                    ],
                    max_length=20,
                    unique=True,
                )),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Notification Workflow",
                "verbose_name_plural": "Notification Workflows",
            },
        ),
        migrations.CreateModel(
            name="WorkflowStage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stage_number", models.IntegerField(help_text="Order of stages (1=first, 2=second, etc.)")),
                ("stage_name", models.CharField(help_text="e.g., 'Department HOD Approval', 'Contact Person Approval'", max_length=100)),
                ("description", models.TextField(blank=True)),
                ("approver_role", models.CharField(blank=True, help_text="Role required to approve (e.g., 'department_hod', 'security'). Leave blank if not approval stage.", max_length=50)),
                ("is_approval_stage", models.BooleanField(default=False, help_text="Is this an approval stage or just notification?")),
                ("notification_type", models.CharField(
                    choices=[
                        ("popup", "Popup Notification"),
                        ("email", "Email Notification"),
                        ("both", "Both Popup & Email"),
                        ("none", "None (Disabled)"),
                    ],
                    default="both",
                    max_length=20,
                )),
                ("send_to_roles", models.CharField(blank=True, help_text="Comma-separated roles to notify (e.g., 'department_hod,security')", max_length=500)),
                ("send_to_employee", models.BooleanField(default=True, help_text="Send notification to pass requester/creator")),
                ("skip_for_management", models.BooleanField(default=False, help_text="Don't send notification if approver is Management role")),
                ("skip_for_plant_head", models.BooleanField(default=False, help_text="Don't send notification if approver is Plant Head role")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("workflow", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stages", to="accounts.notificationworkflow")),
            ],
            options={
                "ordering": ["workflow", "stage_number"],
                "unique_together": {("workflow", "stage_number")},
            },
        ),
        migrations.CreateModel(
            name="WorkflowNotificationRecipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient_role", models.CharField(help_text="Role that should receive notifications", max_length=50)),
                ("is_optional", models.BooleanField(default=False, help_text="Is this a CC/optional recipient?")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("stage", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="extra_recipients", to="accounts.workflowstage")),
            ],
            options={
                "unique_together": {("stage", "recipient_role")},
            },
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="skip_management_notifications",
            field=models.BooleanField(
                default=False,
                help_text="If enabled, Management role will not receive routine notifications (approval-required only)",
                verbose_name="Skip Management Notifications",
            ),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="skip_plant_head_notifications",
            field=models.BooleanField(
                default=False,
                help_text="If enabled, Plant Head role will not receive routine notifications (approval-required only)",
                verbose_name="Skip Plant Head Notifications",
            ),
        ),
    ]
