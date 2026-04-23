from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('session-check/', views.session_check, name='session_check'),
    path('set-hostname/', views.set_hostname, name='set_hostname'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('admin-otp/', views.admin_otp_verify, name='admin_otp_verify'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/set/<str:token>/', views.forgot_password_set, name='forgot_password_set'),
    path('inauguration/', views.inauguration_page, name='inauguration_page'),
    path('settings/', views.system_settings, name='system_settings'),
    path('settings/backup/', views.backup_download, name='backup_download'),
    path('audit-log/', views.audit_log, name='audit_log'),
    path('user-rights-matrix/', views.user_rights_matrix, name='user_rights_matrix'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/import/', views.import_employees, name='import_employees'),
    path('employees/export/', views.export_employees, name='export_employees'),
    path('employees/template/', views.download_template, name='download_template'),
    path('employees/bulk-action/', views.bulk_action, name='bulk_action'),
    
    # Notifications
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('notifications/clear/', views.clear_notifications, name='clear_notifications'),
]

