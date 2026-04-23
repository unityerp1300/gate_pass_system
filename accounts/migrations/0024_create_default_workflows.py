from django.db import migrations


def create_default_workflows(apps, schema_editor):
    """Create default workflow configurations."""
    NotificationWorkflow = apps.get_model('accounts', 'NotificationWorkflow')
    WorkflowStage = apps.get_model('accounts', 'WorkflowStage')
    
    # IGP Workflow
    if not NotificationWorkflow.objects.filter(pass_type='igp').exists():
        igp_workflow = NotificationWorkflow.objects.create(
            pass_type='igp',
            name='Internal Gate Pass Workflow',
            description='Multi-stage approval workflow for internal gate passes'
        )
        
        WorkflowStage.objects.create(
            workflow=igp_workflow,
            stage_number=1,
            stage_name='Department HOD Approval',
            approver_role='department_hod',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='department_hod',
            send_to_employee=True,
        )
        
        WorkflowStage.objects.create(
            workflow=igp_workflow,
            stage_number=2,
            stage_name='HR Approval',
            approver_role='hr',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='hr',
            send_to_employee=False,
        )
        
        WorkflowStage.objects.create(
            workflow=igp_workflow,
            stage_number=3,
            stage_name='Security Approval',
            approver_role='security',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='security',
            send_to_employee=True,
        )
    
    # VGP Workflow
    if not NotificationWorkflow.objects.filter(pass_type='vgp').exists():
        vgp_workflow = NotificationWorkflow.objects.create(
            pass_type='vgp',
            name='Visitor Gate Pass Workflow',
            description='Single-stage approval workflow for visitor gate passes'
        )
        
        WorkflowStage.objects.create(
            workflow=vgp_workflow,
            stage_number=1,
            stage_name='Security Approval',
            approver_role='security',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='security',
            send_to_employee=True,
        )
    
    # MGP Workflow
    if not NotificationWorkflow.objects.filter(pass_type='mgp').exists():
        mgp_workflow = NotificationWorkflow.objects.create(
            pass_type='mgp',
            name='Material Gate Pass Workflow',
            description='Two-stage workflow: Employee → Store HOD → Acknowledge'
        )
        
        WorkflowStage.objects.create(
            workflow=mgp_workflow,
            stage_number=1,
            stage_name='Store HOD Review',
            approver_role='department_hod',
            is_approval_stage=True,
            notification_type='both',
            send_to_roles='department_hod',
            send_to_employee=True,
        )
        
        WorkflowStage.objects.create(
            workflow=mgp_workflow,
            stage_number=2,
            stage_name='Acknowledge',
            approver_role='security',
            is_approval_stage=False,
            notification_type='email',
            send_to_roles='security',
            send_to_employee=True,
        )
    
    # Help Desk Workflow
    if not NotificationWorkflow.objects.filter(pass_type='helpdesk').exists():
        hd_workflow = NotificationWorkflow.objects.create(
            pass_type='helpdesk',
            name='IT Help Desk Workflow',
            description='Ticket assignment and acknowledgment workflow'
        )
        
        WorkflowStage.objects.create(
            workflow=hd_workflow,
            stage_number=1,
            stage_name='IT Department Assignment',
            approver_role='',
            is_approval_stage=False,
            notification_type='email',
            send_to_roles='',
            send_to_employee=True,
        )
        
        WorkflowStage.objects.create(
            workflow=hd_workflow,
            stage_number=2,
            stage_name='Acknowledge',
            approver_role='',
            is_approval_stage=False,
            notification_type='email',
            send_to_roles='',
            send_to_employee=True,
        )


def reverse_workflows(apps, schema_editor):
    """Remove default workflows."""
    NotificationWorkflow = apps.get_model('accounts', 'NotificationWorkflow')
    NotificationWorkflow.objects.filter(
        pass_type__in=['igp', 'vgp', 'mgp', 'helpdesk']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0023_workflow_models"),
    ]

    operations = [
        migrations.RunPython(create_default_workflows, reverse_workflows),
    ]
