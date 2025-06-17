from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Message, StudentProfile, StaffProfile

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Add fields you want to display in the admin interface
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']  # Required for autocomplete_fields

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'sent_at', 'is_read']
    list_filter = ['sent_at', 'is_read', 'sender__is_staff']
    search_fields = ['subject', 'body', 'sender__username', 'sender__email']
    readonly_fields = ['sent_at']
    ordering = ['-sent_at']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'major', 'enrollment_year']
    search_fields = ['user__username', 'user__email', 'student_id', 'major']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'staff_id', 'department', 'position']
    search_fields = ['user__username', 'user__email', 'staff_id', 'department']