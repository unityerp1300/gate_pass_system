from django.db import migrations


def add_workflow_variants(apps, schema_editor):
    """Add additional IGP and VGP workflow variants based on creator role."""
    NotificationWorkflow = apps.get_model('accounts', 'NotificationWorkflow')
    WorkflowStage = apps.get_model('accounts', 'WorkflowStage')
    
    # Get the existing IGP workflow and update it to be for 'employee' creator
    try:
        igp_employee = NotificationWorkflow.objects.filter(pass_type='igp').first()
        if igp_employee:
            # Update existing workflow to explicitly be for employee creator
            igp_employee.creator_role = 'employee'
            igp_employee.name = 'Employee Created IGP'
            igp_employee.description = 'Workflow when Employee creates IGP: Dept HOD → HR → Security'
            igp_employee.save()
    except:
        pass
    
    # Add IGP workflow for Department HOD/HR creation
    # Department HOD/HR Create --> Plant Head --> HR --> Security
    if not NotificationWorkflow.objects.filter(pass_type='igp', creator_role='department_hod').exists():
        igp_hod = NotificationWorkflow.objects.create(
            pass_type='igp',
            creator_role='department_hod',
            name='Department HOD/HR Created IGP',
            description='Workflow when Department HOD or HR creates IGP: Plant Head → HR → Security'
        )
        
        WorkflowStage.objects.create(
            workflow=igp_hod,
            stage_number=1,
            stage_name='Plant Head Approval',
            approver_role='plant_head',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='plant_head',
            send_to_employee=True,
        )
        
        WorkflowStage.objects.create(
            workflow=igp_hod,
            stage_number=2,
            stage_name='HR Approval',
            approver_role='hr',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='hr',
            send_to_employee=False,
        )
        
        WorkflowStage.objects.create(
            workflow=igp_hod,
            stage_number=3,
            stage_name='Security Approval',
            approver_role='security',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='security',
            send_to_employee=True,
        )
    
    # Add IGP workflow for Plant Head creation
    # Plant Head --> Management --> Security
    if not NotificationWorkflow.objects.filter(pass_type='igp', creator_role='plant_head').exists():
        igp_plant = NotificationWorkflow.objects.create(
            pass_type='igp',
            creator_role='plant_head',
            name='Plant Head Created IGP',
            description='Workflow when Plant Head creates IGP: Management → Security'
        )
        
        WorkflowStage.objects.create(
            workflow=igp_plant,
            stage_number=1,
            stage_name='Management Approval',
            approver_role='management',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='management',
            send_to_employee=True,
        )
        
        WorkflowStage.objects.create(
            workflow=igp_plant,
            stage_number=2,
            stage_name='Security Approval',
            approver_role='security',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='security',
            send_to_employee=True,
        )
    
    # Update existing VGP workflow to be for 'security' creator if it doesn't have a creator_role
    vgp = NotificationWorkflow.objects.filter(pass_type='vgp').first()
    if vgp and vgp.creator_role == 'any':
        vgp.creator_role = 'security'
        vgp.name = 'Security Created VGP'
        vgp.description = 'Workflow when Security creates VGP: Contact Person → Security'
        vgp.save()


def remove_workflow_variants(apps, schema_editor):
    """Remove workflow variants added by this migration."""
    NotificationWorkflow = apps.get_model('accounts', 'NotificationWorkflow')
    NotificationWorkflow.objects.filter(
        pass_type='igp',
        creator_role__in=['department_hod', 'plant_head']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0025_notificationworkflow_creator_role"),
    ]

    operations = [
        migrations.RunPython(add_workflow_variants, remove_workflow_variants),
    ]
