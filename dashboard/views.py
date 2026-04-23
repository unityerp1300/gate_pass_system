from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from datetime import date, timedelta
import json
from accounts.models import Employee, SystemSetting
from internal_pass.models import InternalGatePass
from visitor_pass.models import VisitorGatePass
from helpdesk.models import Ticket
from material_pass.models import MaterialGatePass
from grievance.models import Grievance as GrievanceModel


@login_required
def index(request):
    setting = SystemSetting.get()
    
    today = date.today()

    # ── MGP stats ─────────────────────────────────────────────────────────
    mgp_qs = MaterialGatePass.objects
    mgp_today      = mgp_qs.filter(pass_date=today).count()
    mgp_pending    = mgp_qs.filter(status='pending').count()
    mgp_approved   = mgp_qs.filter(status='approved').count()
    mgp_returned   = mgp_qs.filter(status='returned').count()
    mgp_returnable = mgp_qs.filter(is_returnable=True).count()
    mgp_non_ret    = mgp_qs.filter(is_returnable=False).count()
    recent_mgp     = mgp_qs.select_related('employee').order_by('-created_at')[:8]

    mgp_monthly = (mgp_qs
                   .filter(pass_date__gte=today - timedelta(days=180))
                   .annotate(month=TruncMonth('pass_date'))
                   .values('month').annotate(count=Count('id')).order_by('month'))
    mgp_chart_labels = json.dumps([x['month'].strftime('%b %Y') for x in mgp_monthly])
    mgp_chart_data   = json.dumps([x['count'] for x in mgp_monthly])

    mgp_status = mgp_qs.values('status').annotate(count=Count('id'))
    mgp_status_labels = json.dumps([x['status'].title() for x in mgp_status])
    mgp_status_data   = json.dumps([x['count'] for x in mgp_status])

    mgp_type_labels = json.dumps(['Returnable', 'Non-Returnable'])
    mgp_type_data   = json.dumps([mgp_returnable, mgp_non_ret])

    ctx = {
        # ── Employees ──
        'total_employees': Employee.objects.filter(is_active=True).count(),

        # ── IGP ──
        'igp_today':    InternalGatePass.objects.filter(out_date=today).count(),
        'igp_pending':  InternalGatePass.objects.filter(status='pending').count(),
        'igp_approved': InternalGatePass.objects.filter(status='approved').count(),
        'recent_igp':   InternalGatePass.objects.select_related('employee').order_by('-created_at')[:5],

        # ── VGP ──
        'vgp_today':    VisitorGatePass.objects.filter(visit_date=today).count(),
        'vgp_pending':  VisitorGatePass.objects.filter(visit_date=today).count(),
        'vgp_approved': VisitorGatePass.objects.filter(status='approved').count(),
        'recent_vgp':   VisitorGatePass.objects.select_related('person_to_meet').order_by('-created_at')[:5],

        # ── Help Desk ──
        'hd_open':        Ticket.objects.filter(status='open').count(),
        'hd_in_progress': Ticket.objects.filter(status='in_progress').count(),
        'hd_critical':    Ticket.objects.filter(priority='critical', status__in=['open', 'in_progress']).count(),
        'hd_resolved':    Ticket.objects.filter(status='resolved').count(),
        'recent_tickets': Ticket.objects.select_related('raised_by', 'assigned_to').order_by('-created_at')[:8],

        # ── Grievance ──
        'grv_open':     GrievanceModel.objects.filter(status='open').count(),
        'grv_review':   GrievanceModel.objects.filter(status='under_review').count(),
        'grv_resolved': GrievanceModel.objects.filter(status='resolved').count(),
        'grv_critical': GrievanceModel.objects.filter(priority='critical', status__in=['open', 'under_review']).count(),
        'recent_grv':   GrievanceModel.objects.select_related('raised_by').order_by('-created_at')[:8],

        # ── MGP ──
        'mgp_today':      mgp_today,
        'mgp_pending':    mgp_pending,
        'mgp_approved':   mgp_approved,
        'mgp_returned':   mgp_returned,
        'mgp_returnable': mgp_returnable,
        'mgp_non_ret':    mgp_non_ret,
        'recent_mgp':     recent_mgp,
        'mgp_chart_labels':  mgp_chart_labels,
        'mgp_chart_data':    mgp_chart_data,
        'mgp_status_labels': mgp_status_labels,
        'mgp_status_data':   mgp_status_data,
        'mgp_type_labels':   mgp_type_labels,
        'mgp_type_data':     mgp_type_data,
    }

    # ── IGP charts ────────────────────────────────────────────────────────
    igp_monthly = (InternalGatePass.objects
                   .filter(out_date__gte=today - timedelta(days=180))
                   .annotate(month=TruncMonth('out_date'))
                   .values('month').annotate(count=Count('id')).order_by('month'))
    ctx['igp_chart_labels'] = json.dumps([x['month'].strftime('%b %Y') for x in igp_monthly])
    ctx['igp_chart_data']   = json.dumps([x['count'] for x in igp_monthly])

    vgp_monthly = (VisitorGatePass.objects
                   .filter(visit_date__gte=today - timedelta(days=180))
                   .annotate(month=TruncMonth('visit_date'))
                   .values('month').annotate(count=Count('id')).order_by('month'))
    ctx['vgp_chart_labels'] = json.dumps([x['month'].strftime('%b %Y') for x in vgp_monthly])
    ctx['vgp_chart_data']   = json.dumps([x['count'] for x in vgp_monthly])

    igp_status = InternalGatePass.objects.values('status').annotate(count=Count('id'))
    ctx['igp_status_labels'] = json.dumps([x['status'].title() for x in igp_status])
    ctx['igp_status_data']   = json.dumps([x['count'] for x in igp_status])

    vgp_status = VisitorGatePass.objects.values('status').annotate(count=Count('id'))
    ctx['vgp_status_labels'] = json.dumps([x['status'].title() for x in vgp_status])
    ctx['vgp_status_data']   = json.dumps([x['count'] for x in vgp_status])

    return render(request, 'dashboard/index.html', ctx)


@login_required
def hd_stats(request):
    from django.template.loader import render_to_string
    tickets = Ticket.objects.select_related('raised_by', 'assigned_to').order_by('-created_at')[:8]
    tickets_html = render_to_string('dashboard/_hd_ticket_rows.html', {'tickets': tickets}, request=request)
    return JsonResponse({
        'open':        Ticket.objects.filter(status='open').count(),
        'in_progress': Ticket.objects.filter(status='in_progress').count(),
        'critical':    Ticket.objects.filter(priority='critical', status__in=['open', 'in_progress']).count(),
        'resolved':    Ticket.objects.filter(status='resolved').count(),
        'tickets_html': tickets_html,
    })
