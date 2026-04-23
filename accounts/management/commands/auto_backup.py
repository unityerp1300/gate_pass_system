"""
Management command: auto_backup
Runs daily at midnight (via Windows Task Scheduler or cron).
Saves a full JSON backup to BASE_DIR/backups/

Usage:
    python manage.py auto_backup

Schedule (Windows Task Scheduler):
    Program: python
    Arguments: manage.py auto_backup
    Start in: Z:/gate_pass_system
    Trigger: Daily at 00:00
"""
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create automatic daily backup of all ERP data as JSON'

    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        now = timezone.now()
        filename = f'auto_backup_{now.strftime("%Y%m%d_%H%M%S")}.json'
        filepath = os.path.join(backup_dir, filename)

        data = {}

        # Settings
        try:
            from accounts.models import SystemSetting
            setting = SystemSetting.get()
            data['settings'] = {
                f.name: getattr(setting, f.name)
                for f in setting._meta.fields
                if f.name not in ('id',)
            }
            for k, v in data['settings'].items():
                if hasattr(v, 'isoformat'):
                    data['settings'][k] = v.isoformat()
        except Exception as e:
            self.stderr.write(f'Settings backup failed: {e}')

        # Employees
        try:
            from django.core import serializers as dj_serializers
            from accounts.models import Employee
            data['employees'] = json.loads(
                dj_serializers.serialize('json', Employee.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'Employees backup failed: {e}')

        # IGP
        try:
            from internal_pass.models import InternalGatePass, GatePassApproval
            data['igp'] = json.loads(
                dj_serializers.serialize('json', InternalGatePass.objects.all())
            )
            data['igp_approvals'] = json.loads(
                dj_serializers.serialize('json', GatePassApproval.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'IGP backup failed: {e}')

        # VGP
        try:
            from visitor_pass.models import VisitorGatePass
            data['vgp'] = json.loads(
                dj_serializers.serialize('json', VisitorGatePass.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'VGP backup failed: {e}')

        # MGP
        try:
            from material_pass.models import MaterialGatePass, MaterialItem, MaterialRequest
            data['mgp'] = json.loads(
                dj_serializers.serialize('json', MaterialGatePass.objects.all())
            )
            data['mgp_items'] = json.loads(
                dj_serializers.serialize('json', MaterialItem.objects.all())
            )
            data['mgp_requests'] = json.loads(
                dj_serializers.serialize('json', MaterialRequest.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'MGP backup failed: {e}')

        # HD
        try:
            from helpdesk.models import Ticket, TicketComment
            data['hd_tickets'] = json.loads(
                dj_serializers.serialize('json', Ticket.objects.all())
            )
            data['hd_comments'] = json.loads(
                dj_serializers.serialize('json', TicketComment.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'HD backup failed: {e}')

        # Grievance
        try:
            from grievance.models import Grievance, GrievanceComment
            data['grievances'] = json.loads(
                dj_serializers.serialize('json', Grievance.objects.all())
            )
            data['grievance_comments'] = json.loads(
                dj_serializers.serialize('json', GrievanceComment.objects.all())
            )
        except Exception as e:
            self.stderr.write(f'Grievance backup failed: {e}')

        data['_meta'] = {
            'backup_type': 'auto_daily',
            'created_at': now.isoformat(),
            'version': '1.0',
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        # Keep only last 30 backups
        try:
            backups = sorted([
                f for f in os.listdir(backup_dir)
                if f.startswith('auto_backup_') and f.endswith('.json')
            ])
            while len(backups) > 30:
                os.remove(os.path.join(backup_dir, backups.pop(0)))
        except Exception:
            pass

        size_kb = os.path.getsize(filepath) // 1024
        self.stdout.write(self.style.SUCCESS(
            f'Backup created: {filename} ({size_kb} KB)'
        ))
