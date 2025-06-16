from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os


User = get_user_model()

def get_upload_path(instance, filename):
    """Generate upload path for course documents"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename with course code and original name
    filename = f"{instance.course.course_code}_{slugify(instance.title)}.{ext}"
    # Create path: course_documents/department_code/course_code/filename
    return os.path.join('course_documents', instance.course.department.code, instance.course.course_code, filename)


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

    class Meta:
        ordering = ['name']


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

    class Meta:
        ordering = ['title']


class CourseDocument(models.Model):
    """
    Model for course materials like PDF, Excel, Word documents, and images.
    """
    DOCUMENT_TYPES = (
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document (.doc)'),
        ('docx', 'Word Document (.docx)'),
        ('xls', 'Excel Spreadsheet (.xls)'),
        ('xlsx', 'Excel Spreadsheet (.xlsx)'),
        ('ppt', 'PowerPoint Presentation (.ppt)'),
        ('pptx', 'PowerPoint Presentation (.pptx)'),
        ('txt', 'Text Document'),
        ('csv', 'CSV File'),
        ('zip', 'ZIP Archive'),
        ('rar', 'RAR Archive'),
        ('jpg', 'JPEG Image'),
        ('jpeg', 'JPEG Image'),
        ('png', 'PNG Image'),
        ('gif', 'GIF Image'),
        ('other', 'Other Format'),
    )
    
    title = models.CharField(max_length=255, help_text="Enter a descriptive title for the document")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 
                    'txt', 'csv', 'zip', 'rar', 'jpg', 'jpeg', 'png', 'gif'
                ]
            )
        ],
        help_text="Supported formats: PDF, Word, Excel, PowerPoint, Text, CSV, ZIP, RAR, Images"
    )
    description = models.TextField(blank=True, null=True, help_text="Optional description of the document content")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size in bytes")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this document from students")

    def save(self, *args, **kwargs):
        # Auto-detect document type based on file extension
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            # Map extensions to document types
            ext_mapping = {
                'pdf': 'pdf',
                'doc': 'doc',
                'docx': 'docx',
                'xls': 'xls',
                'xlsx': 'xlsx',
                'ppt': 'ppt',
                'pptx': 'pptx',
                'txt': 'txt',
                'csv': 'csv',
                'zip': 'zip',
                'rar': 'rar',
                'jpg': 'jpg',
                'jpeg': 'jpeg',
                'png': 'png',
                'gif': 'gif',
            }
            self.document_type = ext_mapping.get(ext, 'other')
            
            # Set file size
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

    @property
    def file_size_mb(self):
        """Return file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Course Document"
        verbose_name_plural = "Course Documents"


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
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"