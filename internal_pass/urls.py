from django.urls import path
from . import views

app_name = 'internal_pass'

urlpatterns = [
    path('', views.pass_list, name='pass_list'),
    path('create/', views.pass_create, name='pass_create'),
    path('<int:pk>/', views.pass_detail, name='pass_detail'),
    path('<int:pk>/approve/', views.pass_approve, name='pass_approve'),
    path('<int:pk>/return/', views.mark_returned, name='mark_returned'),
    path('<int:pk>/print/', views.print_pass, name='print_pass'),
    path('stage-action/<str:token>/<str:action>/', views.stage_action, name='stage_action'),
    path('bulk-action/', views.bulk_action, name='bulk_action'),
    path('report/daily/', views.daily_report, name='daily_report'),
    path('report/monthly/', views.monthly_report, name='monthly_report'),
    path('report/export/', views.export_report, name='export_report'),
    path('report/export-pdf/', views.export_report_pdf, name='export_report_pdf'),
]

