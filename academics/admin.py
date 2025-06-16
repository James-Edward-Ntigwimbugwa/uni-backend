from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Department, Course, CourseDocument, StudentCourseEnrollment


class CourseDocumentInline(admin.TabularInline):
    """Inline admin for course documents"""
    model = CourseDocument
    extra = 1
    fields = ('title', 'file', 'document_type', 'description', 'is_active')
    readonly_fields = ('document_type', 'uploaded_by', 'uploaded_at', 'file_size')
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course_count', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Number of Courses'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_code', 'department', 'document_count', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('title', 'course_code', 'description')
    autocomplete_fields = ('department',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CourseDocumentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'course_code', 'department', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon_name', 'color_code'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def document_count(self, obj):
        count = obj.documents.filter(is_active=True).count()
        if count > 0:
            url = reverse('admin:academics_coursedocument_changelist') + f'?course={obj.id}'
            return format_html('<a href="{}">{} documents</a>', url, count)
        return '0 documents'
    document_count.short_description = 'Documents'


@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'document_type', 'file_size_display', 'uploaded_by', 'is_active', 'uploaded_at')
    list_filter = ('document_type', 'is_active', 'course__department', 'uploaded_at')
    search_fields = ('title', 'description', 'course__title', 'course__course_code')
    autocomplete_fields = ('course', 'uploaded_by')
    readonly_fields = ('document_type', 'uploaded_by', 'uploaded_at', 'updated_at', 'file_size', 'file_preview')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'course', 'file', 'document_type', 'description', 'is_active')
        }),
        ('File Details', {
            'fields': ('file_preview', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def file_size_display(self, obj):
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} bytes"
            elif obj.file_size < 1024 * 1024:
                return f"{round(obj.file_size / 1024, 1)} KB"
            else:
                return f"{round(obj.file_size / (1024 * 1024), 1)} MB"
        return "Unknown"
    file_size_display.short_description = 'File Size'
    
    def file_preview(self, obj):
        if obj.file:
            file_url = obj.file.url
            file_name = obj.file.name.split('/')[-1]
            
            # Create different previews based on file type
            if obj.document_type in ['jpg', 'jpeg', 'png', 'gif']:
                return format_html(
                    '<img src="{}" style="max-width: 200px; max-height: 150px;" alt="{}"/><br>'
                    '<a href="{}" target="_blank">View Full Size</a>',
                    file_url, file_name, file_url
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank" class="button">📄 Download {}</a>',
                    file_url, file_name
                )
        return "No file uploaded"
    file_preview.short_description = 'File Preview'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'course__department', 'uploaded_by')


@admin.register(StudentCourseEnrollment)
class StudentCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'course_department', 'enrolled_at', 'is_active')
    list_filter = ('is_active', 'enrolled_at', 'course__department')
    search_fields = ('student__username', 'student__email', 'course__title', 'course__course_code')
    autocomplete_fields = ('student', 'course')
    readonly_fields = ('enrolled_at',)
    
    def course_department(self, obj):
        return obj.course.department.name
    course_department.short_description = 'Department'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course', 'course__department')


# Customize admin site headers
admin.site.site_header = "Academics Administration"
admin.site.site_title = "Academics Admin"
admin.site.index_title = "Welcome to Academics Administration"