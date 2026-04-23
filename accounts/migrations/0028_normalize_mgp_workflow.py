from django.db import migrations


def normalize_mgp_workflow(apps, schema_editor):
    NotificationWorkflow = apps.get_model('accounts', 'NotificationWorkflow')
    WorkflowStage = apps.get_model('accounts', 'WorkflowStage')

    workflows = NotificationWorkflow.objects.filter(pass_type='mgp')
    for workflow in workflows:
        workflow.name = 'Material Gate Pass Workflow'
        workflow.description = 'Creator to Store HOD approval only'
        workflow.is_active = True
        workflow.save(update_fields=['name', 'description', 'is_active'])

        first_stage, _ = WorkflowStage.objects.get_or_create(
            workflow=workflow,
            stage_number=1,
            defaults={
                'stage_name': 'Store HOD Review',
                'description': 'Store HOD approval stage for MGP',
                'approver_role': 'department_hod',
                'is_approval_stage': True,
                'notification_type': 'email',
                'send_to_roles': 'department_hod',
                'send_to_employee': True,
            },
        )

        first_stage.stage_name = 'Store HOD Review'
        first_stage.description = 'Store HOD approval stage for MGP'
        first_stage.approver_role = 'department_hod'
        first_stage.is_approval_stage = True
        first_stage.notification_type = 'email'
        first_stage.send_to_roles = 'department_hod'
        first_stage.send_to_employee = True
        first_stage.skip_for_management = False
        first_stage.skip_for_plant_head = False
        first_stage.save(
            update_fields=[
                'stage_name',
                'description',
                'approver_role',
                'is_approval_stage',
                'notification_type',
                'send_to_roles',
                'send_to_employee',
                'skip_for_management',
                'skip_for_plant_head',
            ]
        )

        WorkflowStage.objects.filter(workflow=workflow).exclude(stage_number=1).delete()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_alter_notificationworkflow_pass_type'),
    ]

    operations = [
        migrations.RunPython(normalize_mgp_workflow, noop_reverse),
    ]
