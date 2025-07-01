from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import CourseNote, Department, Course, CourseDocument, StudentCourseEnrollment
from .serializers import (
    CourseNoteSerializer,
    DepartmentSerializer, 
    CourseSerializer, 
    CourseDocumentSerializer, 
    StudentCourseEnrollmentSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for university departments
    """
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created_at']


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for university courses
    """
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'module_code', 'department__name']
    ordering_fields = ['title', 'module_code', 'department__name', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department')
        department_code = self.request.query_params.get('department_code')
        
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if department_code:
            queryset = queryset.filter(department__code=department_code)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll the current user in this course"""
        course = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Check if already enrolled
        if StudentCourseEnrollment.objects.filter(student=user, course=course).exists():
            return Response(
                {"error": "Already enrolled in this course"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        enrollment = StudentCourseEnrollment.objects.create(
            student=user,
            course=course
        )
        
        serializer = StudentCourseEnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for course documents (PDF, Word, Excel, etc.)
    """
    queryset = CourseDocument.objects.all().order_by('-uploaded_at')
    serializer_class = CourseDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'document_type', 'course__title']
    ordering_fields = ['title', 'document_type', 'uploaded_at']
    
   
    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        if not course_id:
            # Only allow searching when course is specified
            raise ValidationError({"error": "course query parameter is required"})
        
        queryset = super().get_queryset().filter(course_id=course_id)
        document_type = self.request.query_params.get('type')
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CourseNoteViewSet(viewsets.ModelViewSet):
    queryset = CourseNote.objects.filter(is_active=True)
    serializer_class = CourseNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CourseNote.objects.filter(is_active=True)
        course_id = self.request.query_params.get('course', None)
        category = self.request.query_params.get('category', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
            
        return queryset.order_by('order', '-created_at')

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured notes across all courses"""
        featured_notes = CourseNote.objects.filter(is_featured=True, is_active=True)
        serializer = self.get_serializer(featured_notes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """Get notes grouped by course"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        notes = CourseNote.objects.filter(course_id=course_id, is_active=True)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for student enrollments
    """
    queryset = StudentCourseEnrollment.objects.all().order_by('-enrolled_at')
    serializer_class = StudentCourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return StudentCourseEnrollment.objects.all()
        return StudentCourseEnrollment.objects.filter(student=user)
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Get all courses the current user is enrolled in"""
        user = request.user
        enrollments = StudentCourseEnrollment.objects.filter(
            student=user,
            is_active=True
        )
        courses = [enrollment.course for enrollment in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)