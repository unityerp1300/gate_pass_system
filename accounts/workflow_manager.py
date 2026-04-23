"""
Workflow Manager Service

Handles:
- Getting workflows for pass types
- Determining next approvers in a workflow
- Getting notification recipients for each stage
- Checking if user/role should receive notifications
- Managing workflow advancement logic
"""

from django.db.models import Q
from .models import NotificationWorkflow, WorkflowStage, Employee, SystemSetting


class WorkflowManager:
    """Manages email and notification workflows for different pass types."""
    
    PASS_TYPES = {
        'igp': 'Internal Gate Pass (IGP)',
        'vgp': 'Visitor Gate Pass (VGP)',
        'mgp': 'Material Gate Pass (MGP)',
        'helpdesk': 'IT Help Desk',
    }
    
    @staticmethod
    def get_workflow(pass_type, creator_role=None):
        """
        Get the workflow definition for a pass type.
        
        Args:
            pass_type: Type of pass ('igp', 'vgp', 'mgp', 'helpdesk')
            creator_role: Role of the pass creator ('employee', 'department_hod', etc.)
                         If None, tries to find creator-specific workflow first, then defaults to 'any'
        
        Returns:
            NotificationWorkflow instance or None
        """
        try:
            if creator_role:
                # Try to get workflow for specific creator role
                workflow = NotificationWorkflow.objects.get(
                    pass_type=pass_type, 
                    creator_role=creator_role, 
                    is_active=True
                )
                return workflow
            else:
                # Try specific role workflows first, then fall back to 'any'
                workflow = NotificationWorkflow.objects.filter(
                    pass_type=pass_type, 
                    is_active=True
                ).exclude(creator_role='any').first()
                
                if not workflow:
                    workflow = NotificationWorkflow.objects.get(
                        pass_type=pass_type, 
                        creator_role='any', 
                        is_active=True
                    )
                return workflow
        except NotificationWorkflow.DoesNotExist:
            return None
    
    @staticmethod
    def get_workflow_stages(pass_type, creator_role=None):
        """Get all stages for a workflow in order."""
        workflow = WorkflowManager.get_workflow(pass_type, creator_role)
        if not workflow:
            return []
        return list(workflow.stages.all().order_by('stage_number'))
    
    @staticmethod
    def get_next_stage(pass_type, current_stage_number, creator_role=None):
        """Get the next stage in the workflow."""
        workflow = WorkflowManager.get_workflow(pass_type, creator_role)
        if not workflow:
            return None
        
        try:
            next_stage = workflow.stages.get(stage_number=current_stage_number + 1)
            return next_stage
        except WorkflowStage.DoesNotExist:
            return None  # No more stages
    
    @staticmethod
    def get_notification_recipients(stage, pass_creator=None, current_approver=None):
        """
        Get list of employees who should receive notification for a stage.
        
        Args:
            stage: WorkflowStage instance
            pass_creator: Employee instance who created the pass
            current_approver: Employee instance of current approver (if any)
        
        Returns:
            List of Employee instances to notify
        """
        settings = SystemSetting.get()
        recipients = set()
        
        # Add pass creator if enabled
        if stage.send_to_employee and pass_creator:
            recipients.add(pass_creator)
        
        # Get roles to notify
        notification_roles = stage.get_notification_roles()
        if notification_roles:
            employees = Employee.objects.filter(role__in=notification_roles, is_active=True)
            if stage.workflow.pass_type == 'mgp' and stage.approver_role == 'department_hod':
                employees = employees.filter(department='Store')
            
            # Filter out management/plant head if configured
            if settings.skip_management_notifications:
                employees = employees.exclude(role='management')
            if settings.skip_plant_head_notifications:
                employees = employees.exclude(role='president_plant_head')
            
            recipients.update(employees)
        
        # Add extra recipients from fine-grained config
        extra_recipients = stage.extra_recipients.all()
        for extra in extra_recipients:
            employees = Employee.objects.filter(role=extra.recipient_role, is_active=True)
            recipients.update(employees)
        
        # Remove current approver if they're in recipients (unless explicitly requested)
        if current_approver:
            recipients.discard(current_approver)
        
        return list(recipients)
    
    @staticmethod
    def should_send_notification(stage, recipient_user, pass_type):
        """
        Check if notification should be sent to a user for this stage.
        
        Args:
            stage: WorkflowStage instance
            recipient_user: Employee instance to check
            pass_type: str (igp, vgp, mgp, helpdesk)
        
        Returns:
            Dict with 'popup' and 'email' keys (True/False for each channel)
        """
        settings = SystemSetting.get()
        
        # Check if user should receive this based on role skip settings
        if settings.skip_management_notifications and recipient_user.has_role('management'):
            return {'popup': False, 'email': False}
        
        if settings.skip_plant_head_notifications and recipient_user.has_role('president_plant_head'):
            return {'popup': False, 'email': False}
        
        # Check notification type setting
        notification_type = stage.notification_type
        
        # Check global notification channel settings
        popup_enabled = getattr(settings, f'notif_{pass_type}_popup', True)
        email_enabled = getattr(settings, f'notif_{pass_type}_email', True)
        
        # Determine which channels should be used
        channels = {'popup': False, 'email': False}
        
        if notification_type == 'popup':
            channels['popup'] = popup_enabled
        elif notification_type == 'email':
            channels['email'] = email_enabled
        elif notification_type == 'both':
            channels['popup'] = popup_enabled
            channels['email'] = email_enabled
        # 'none' means no notifications (both stay False)
        
        return channels
    
    @staticmethod
    def get_approval_recipients(stage):
        """Get employees who can approve at this stage."""
        if not stage.is_approval_stage:
            return []
        
        if stage.approver_role:
            employees = Employee.objects.filter(
                role=stage.approver_role,
                is_active=True
            )
            if stage.workflow.pass_type == 'mgp' and stage.approver_role == 'department_hod':
                employees = employees.filter(department='Store')
            return list(employees)
        
        return []
    
    @staticmethod
    def advance_workflow(pass_instance, current_stage, action='approve', remarks=''):
        """
        Advance workflow to next stage or complete it.
        
        Args:
            pass_instance: The pass object (InternalGatePass, VisitorGatePass, etc.)
            current_stage: Current WorkflowStage
            action: 'approve' or 'reject'
            remarks: Optional approval/rejection remarks
        
        Returns:
            Dict with keys: success (bool), message (str), next_stage (WorkflowStage or None)
        """
        pass_type = pass_instance._meta.app_label.split('_')[0] if '_' in pass_instance._meta.app_label else pass_instance._meta.app_label
        
        if action == 'reject':
            # Set pass status to rejected and stop workflow
            pass_instance.status = 'rejected'
            pass_instance.save()
            return {
                'success': True,
                'message': 'Pass rejected',
                'next_stage': None
            }
        
        elif action == 'approve':
            next_stage = WorkflowManager.get_next_stage(pass_type, current_stage.stage_number)
            
            if next_stage:
                # Move to next stage
                if hasattr(pass_instance, 'current_stage'):
                    pass_instance.current_stage = next_stage.stage_number
                pass_instance.status = 'in_progress'
                pass_instance.save()
                
                return {
                    'success': True,
                    'message': f'Approved. Forwarded to {next_stage.stage_name}',
                    'next_stage': next_stage
                }
            else:
                # All stages completed
                pass_instance.status = 'approved'
                pass_instance.save()
                
                return {
                    'success': True,
                    'message': 'Fully Approved',
                    'next_stage': None
                }
        
        return {
            'success': False,
            'message': 'Invalid action',
            'next_stage': None
        }
    
    @staticmethod
    def create_default_workflows():
        """Create default workflow configurations if they don't exist."""
        
        # IGP Workflow
        if not NotificationWorkflow.objects.filter(pass_type='igp').exists():
            igp_workflow = NotificationWorkflow.objects.create(
                pass_type='igp',
                name='Internal Gate Pass Workflow',
                description='Multi-stage approval workflow for internal gate passes'
            )
            
            stages_data = [
                {
                    'stage_number': 1,
                    'stage_name': 'Department HOD Approval',
                    'approver_role': 'department_hod',
                    'is_approval_stage': True,
                    'notification_type': 'both',
                    'send_to_roles': 'department_hod',
                    'send_to_employee': True,
                },
                {
                    'stage_number': 2,
                    'stage_name': 'HR Approval',
                    'approver_role': 'hr',
                    'is_approval_stage': True,
                    'notification_type': 'both',
                    'send_to_roles': 'hr',
                    'send_to_employee': False,
                },
                {
                    'stage_number': 3,
                    'stage_name': 'Security Approval',
                    'approver_role': 'security',
                    'is_approval_stage': True,
                    'notification_type': 'both',
                    'send_to_roles': 'security',
                    'send_to_employee': True,
                },
            ]
            
            for stage_data in stages_data:
                stage_data['workflow'] = igp_workflow
                WorkflowStage.objects.create(**stage_data)
        
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
                approver_role='',  # Not an approval stage
                is_approval_stage=False,
                notification_type='email',
                send_to_roles='',  # IT staff notified via ticket assignment
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
