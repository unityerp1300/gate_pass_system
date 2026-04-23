"""
Simplified notification service — email only, no popup system.
Recipients are determined by the workflow_email_recipients setting per module.
"""
import json
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import EmailLog, Employee, SystemSetting


def _get_email_recipients(module_key):
    """Return list of Employee objects to email for a given module based on settings."""
    setting = SystemSetting.get()
    try:
        recipients_map = json.loads(setting.workflow_email_recipients or '{}')
    except Exception:
        recipients_map = {}
    roles = recipients_map.get(module_key, [])
    if not roles:
        return Employee.objects.none()
    qs = Employee.objects.filter(is_active=True, email__gt='')
    # Filter by any of the configured roles
    from django.db.models import Q
    role_q = Q()
    for role in roles:
        role_q |= Q(role=role)
        role_q |= Q(additional_roles__contains=f'|{role}|')
    return qs.filter(role_q).distinct()


def send_workflow_notification(
    module_key,
    notification_type,
    title,
    description='',
    related_id='',
    related_module='',
    requester=None,
    extra_users=None,
    workflow_stage=None,
):
    """
    Send email notifications for workflow events.
    Recipients are determined by the workflow_email_recipients setting.
    Always sends to requester (pass creator) as well.
    """
    recipients = set(_get_email_recipients(module_key))

    # Always include the requester
    if requester and getattr(requester, 'is_active', False) and requester.email:
        recipients.add(requester)

    # Include any extra explicitly passed users
    if extra_users:
        for user in extra_users:
            if user and getattr(user, 'is_active', False) and user.email:
                recipients.add(user)

    subject = f'{(related_module or module_key).upper()} — {title}'
    body = f'{description}\n\nReference: {related_id}\n\nThis is an automated notification from the ERP System.'

    for user in recipients:
        if not user.email:
            continue
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            EmailLog.objects.create(
                recipient=user.email,
                subject=subject,
                message=description,
                channel=(module_key or 'system').lower(),
                status='sent',
                related_id=related_id,
                related_module=related_module,
            )
        except Exception as e:
            EmailLog.objects.create(
                recipient=user.email,
                subject=subject,
                message=description,
                channel=(module_key or 'system').lower(),
                status='failed',
                related_id=related_id,
                related_module=related_module,
                error=str(e),
            )
