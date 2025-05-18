from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Department, Course, CourseDocument, StudentCourseEnrollment
import tempfile
from PIL import Image


class DepartmentModelTests(TestCase):
    def test_department_creation(self):
        department = Department.objects.create(
            name="Test Department",
            code="TEST"
        )
        self.assertEqual(department.name, "Test Department")
        self.assertEqual(department.code, "TEST")


class CourseModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            code="TEST"
        )
    
    def test_course_creation(self):
        course = Course.objects.create(
            title="Test Course",
            course_code="TST-101",
            department=self.department,
            icon_name="test_icon",
            color_code="#FF5733"
        )
        self.assertEqual(course.title, "Test Course")
        self.assertEqual(course.course_code, "TST-101")
        self.assertEqual(course.department, self.department)


class DocumentModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            code="TEST"
        )
        self.course = Course.objects.create(
            title="Test Course",
            course_code="TST-101",
            department=self.department
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
    
    def test_document_creation(self):
        document = CourseDocument.objects.create(
            title="Test Document",
            course=self.course,
            document_type="pdf",
            uploaded_by=self.user,
            description="Test description"
        )
        self.assertEqual(document.title, "Test Document")
        self.assertEqual(document.course, self.course)
        self.assertEqual(document.document_type, "pdf")
        self.assertEqual(document.uploaded_by, self.user)


class EnrollmentModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            code="TEST"
        )
        self.course = Course.objects.create(
            title="Test Course",
            course_code="TST-101",
            department=self.department
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
    
    def test_enrollment_creation(self):
        enrollment = StudentCourseEnrollment.objects.create(
            student=self.user,
            course=self.course,
            is_active=True
        )
        self.assertEqual(enrollment.student, self.user)
        self.assertEqual(enrollment.course, self.course)
        self.assertTrue(enrollment.is_active)


class APITests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        
        # Create test department
        self.department = Department.objects.create(
            name="Test Department",
            code="TEST",
            description="Test Department Description"
        )
        
        # Create test course
        self.course = Course.objects.create(
            title="Test Course",
            course_code="TST-101",
            department=self.department,
            description="Test Course Description",
            icon_name="test_icon",
            color_code="#FF5733"
        )
        
        # Set up API client
        self.client = APIClient()
        
    def authenticate(self):
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    
    def test_list_departments(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_list_courses(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_filter_courses_by_department(self):
        response = self.client.get(f'/api/courses/?department={self.department.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_enroll_in_course(self):
        self.authenticate()
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check enrollment exists
        enrollment = StudentCourseEnrollment.objects.filter(
            student=self.user,
            course=self.course
        ).exists()
        self.assertTrue(enrollment)
        
    def test_my_courses(self):
        # Create enrollment
        StudentCourseEnrollment.objects.create(
            student=self.user,
            course=self.course,
            is_active=True
        )
        
        # Test API endpoint
        self.authenticate()
        response = self.client.get('/api/enrollments/my_courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.course.title)