from django.urls import path
from . import views

app_name = 'material_pass'

urlpatterns = [
    path('', views.pass_list, name='pass_list'),
    path('create/', views.pass_create, name='pass_create'),
    path('<int:pk>/', views.pass_detail, name='pass_detail'),
    path('<int:pk>/approve/', views.pass_approve, name='pass_approve'),
    path('<int:pk>/edit/', views.pass_edit, name='pass_edit'),
    path('<int:pk>/return/', views.mark_returned, name='mark_returned'),
    path('<int:pk>/print/', views.print_pass, name='print_pass'),
    path('token-action/<str:token>/<str:action>/', views.token_action, name='token_action'),
    path('bulk-action/', views.bulk_action, name='bulk_action'),
    # Material Request
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.request_create, name='request_create'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/review/', views.request_review, name='request_review'),
    path('requests/<int:pk>/convert/', views.request_convert, name='request_convert'),
    path('requests/bulk-action/', views.request_bulk_action, name='request_bulk_action'),
    # Reports
    path('report/daily/', views.daily_report, name='daily_report'),
    path('report/monthly/', views.monthly_report, name='monthly_report'),
    path('report/export/', views.export_report, name='export_report'),
    path('report/export-pdf/', views.export_report_pdf, name='export_report_pdf'),
]

