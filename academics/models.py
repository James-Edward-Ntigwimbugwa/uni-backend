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
    filename = f"{instance.course.module_code}_{slugify(instance.title)}.{ext}"
    # Create path: course_documents/department_code/course_code/filename
    return os.path.join('course_documents', instance.course.department.code, instance.course.module_code, filename)


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
    module_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True, 
                                help_text="Icon name from Flutter Icons class")
    color_code = models.CharField(max_length=10, blank=True, null=True, 
                                 help_text="Color code for the course card")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.module_code})"

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


class CourseNote(models.Model):
    """
    Model for static notes added by teachers for specific courses.
    These are text-based notes explaining concepts, not file uploads.
    """
    NOTE_CATEGORIES = (
        ('lecture', 'Lecture Notes'),
        ('concept', 'Concept Explanation'),
        ('tutorial', 'Tutorial'),
        ('assignment', 'Assignment Guidelines'),
        ('exam_prep', 'Exam Preparation'),
        ('reference', 'Reference Material'),
        ('announcement', 'Course Announcement'),
        ('other', 'Other'),
    )
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    title = models.CharField(max_length=255, help_text="Enter a descriptive title for the note")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    category = models.CharField(max_length=20, choices=NOTE_CATEGORIES, default='lecture',
                               help_text="Categorize the type of note")
    difficulty_level = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default='beginner',
                                       help_text="Difficulty level of the content")
    content = models.TextField(help_text="Write your note content here")
    tags = models.CharField(max_length=200, blank=True, null=True,
                           help_text="Comma-separated tags (e.g., python, loops, functions)")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured to highlight important notes")
    order = models.PositiveIntegerField(default=0, help_text="Order of display (lower numbers appear first)")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this note from students")
    
    # Optional fields for better organization
    chapter = models.CharField(max_length=100, blank=True, null=True,
                              help_text="Chapter or section name (optional)")
    estimated_read_time = models.PositiveIntegerField(blank=True, null=True,
                                                     help_text="Estimated reading time in minutes")

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def word_count(self):
        """Calculate approximate word count of the note content"""
        if self.content:
            return len(self.content.split())
        return 0
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def save(self, *args, **kwargs):
        # Auto-calculate estimated read time if not provided (average 200 words per minute)
        if not self.estimated_read_time and self.content:
            word_count = self.word_count
            self.estimated_read_time = max(1, round(word_count / 200))
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Course Note"
        verbose_name_plural = "Course Notes"
        indexes = [
            models.Index(fields=['course', 'category']),
            models.Index(fields=['course', 'is_featured']),
            models.Index(fields=['course', 'order']),
        ]


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