from django.contrib import admin
from .models import MaterialGatePass, MaterialItem, MaterialAttachment


class MaterialItemInline(admin.TabularInline):
    model = MaterialItem
    extra = 1


class MaterialAttachmentInline(admin.TabularInline):
    model = MaterialAttachment
    extra = 0
    readonly_fields = ['file_name', 'uploaded_at']


@admin.register(MaterialGatePass)
class MaterialGatePassAdmin(admin.ModelAdmin):
    list_display  = ['pass_number', 'employee', 'department', 'direction', 'is_returnable', 'party_name', 'pass_date', 'status']
    list_filter   = ['status', 'direction', 'is_returnable', 'department']
    search_fields = ['pass_number', 'employee__employee_name', 'party_name']
    inlines       = [MaterialItemInline, MaterialAttachmentInline]
