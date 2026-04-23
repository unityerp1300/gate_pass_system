from django.contrib import admin
from .models import Employee, Notification, NotificationPermission

admin.site.register(Employee)


@admin.register(NotificationPermission)
class NotificationPermissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'scope', 'notification_type', 'can_receive', 'can_view_own', 'can_view_department', 'can_view_all', 'updated_at')
    list_filter = ('scope', 'notification_type', 'can_receive', 'can_view_own', 'can_view_department', 'can_view_all')
    search_fields = ('role', 'employee__username', 'department')
    fieldsets = (
        ('Scope', {
            'fields': ('scope', 'role', 'employee', 'department')
        }),
        ('Notification Type', {
            'fields': ('notification_type',)
        }),
        ('Permissions', {
            'fields': ('can_receive', 'can_view_own', 'can_view_department', 'can_view_all'),
            'description': 'Configure what this role/employee/department can do with notifications'
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            # Add readonly fields when editing
            return fieldsets + (('Metadata', {'fields': ('created_at', 'updated_at')}),)
        return fieldsets

