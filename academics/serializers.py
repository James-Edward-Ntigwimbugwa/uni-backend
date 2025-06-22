from rest_framework import serializers
from .models import Department, Course, CourseDocument, StudentCourseEnrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CourseDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CourseDocument
        fields = ['id', 'title', 'document_type', 'file', 'description', 
                  'uploaded_by', 'uploaded_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    documents = CourseDocumentSerializer(many=True, read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'module_code', 'department', 'department_name',
                  'description', 'icon_name', 'color_code', 'documents',
                  'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'logo', 
                  'courses', 'created_at', 'updated_at']


class StudentCourseEnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = StudentCourseEnrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'is_active']