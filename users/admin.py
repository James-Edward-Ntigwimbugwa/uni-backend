from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from .models import StudentProfile, StaffProfile, Message

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_student', 'is_staff', 'is_active')
    list_filter = ('is_student', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'profile_photo')
        }),
        ('Status', {
            'fields': ('is_student', 'is_active')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('last_login', 'date_joined')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_name', 'major', 'enrollment_year')
    list_filter = ('major', 'enrollment_year')
    search_fields = ('student_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__last_name'


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'get_name', 'department', 'position')
    list_filter = ('department', 'position')
    search_fields = ('staff_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__last_name'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender_name', 'recipient_name', 'sent_at', 'is_read', 'message_preview')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('subject', 'body', 'sender__email', 'recipient__email')
    date_hierarchy = 'sent_at'
    readonly_fields = ('sent_at',)
    
    def sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"
    sender_name.short_description = 'Sender'
    sender_name.admin_order_field = 'sender__last_name'
    
    def recipient_name(self, obj):
        return f"{obj.recipient.first_name} {obj.recipient.last_name}"
    recipient_name.short_description = 'Recipient'
    recipient_name.admin_order_field = 'recipient__last_name'
    
    def message_preview(self, obj):
        if len(obj.body) > 50:
            return f"{obj.body[:50]}..."
        return obj.body
    message_preview.short_description = 'Message'