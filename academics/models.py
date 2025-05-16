from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


User = get_user_model()
class Department(models.Model):
    """
    Department model to represent university departments such as Engineering, Business, Technology, etc.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='department_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(models.Model):
    """
    Course model representing university courses like Information Technology, Railway Engineering, etc.
    """
    title = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True, 
                                help_text="Icon name from Flutter Icons class")
    color_code = models.CharField(max_length=10, blank=True, null=True, 
                                 help_text="Color code for the course card")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course_code})"


class CourseDocument(models.Model):
    """
    Model for course materials like PDF, Excel, Word documents, and images.
    """
    DOCUMENT_TYPES = (
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('xlsx', 'Excel Spreadsheet'),
        ('ppt', 'PowerPoint'),
        ('img', 'Image'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='course_documents/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'jpg', 'jpeg', 'png']
            )
        ]
    )
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class StudentCourseEnrollment(models.Model):
    """
    Model to track student enrollments in courses
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"