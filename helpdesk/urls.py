from django.urls import path
from . import views

app_name = 'helpdesk'

urlpatterns = [
    path('',                    views.dashboard,     name='dashboard'),
    path('tickets/',            views.ticket_list,   name='ticket_list'),
    path('tickets/new/',        views.ticket_create, name='ticket_create'),
    path('tickets/<int:pk>/',   views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/close/', views.ticket_close, name='ticket_close'),
    path('tickets/bulk-action/', views.bulk_action, name='bulk_action'),
    path('report/export/', views.export_report, name='export_report'),
    path('report/export-pdf/', views.export_report_pdf, name='export_report_pdf'),
]

