from django.contrib import admin
from .models import Department, Course, CourseDocument, StudentCourseEnrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_code', 'department', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('title', 'course_code', 'description')
    autocomplete_fields = ('department',)


@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('document_type', 'course__department', 'uploaded_at')
    search_fields = ('title', 'description', 'course__title')
    autocomplete_fields = ('course', 'uploaded_by')


@admin.register(StudentCourseEnrollment)
class StudentCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_active')
    list_filter = ('is_active', 'enrolled_at', 'course__department')
    search_fields = ('student__username', 'student__email', 'course__title')
    autocomplete_fields = ('student', 'course')