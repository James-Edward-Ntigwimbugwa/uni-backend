from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from academics.models import Course, Department


User = get_user_model()

#allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png']
class Command(BaseCommand):
    help = 'Seeds the database with initial departments and courses'

    def handle(self, *args, **kwargs):
        # Create superuser with EMAIL and PASSWORD only
        if not User.objects.filter(email='admin@esterMollel.com').exists():
            User.objects.create_superuser(
                email='esterMollel@gmail.com',
                password='esterMollel2001'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        
        # Create departments
        departments = [
            {'name': 'Engineering', 'code': 'ENG'},
            {'name': 'Business', 'code': 'BUS'},
            {'name': 'Technology', 'code': 'TECH'},
            {'name': 'Transportation', 'code': 'TRANS'},
        ]
        
        created_departments = {}
        for dept in departments:
            department, created = Department.objects.get_or_create(
                code=dept['code'],
                defaults={'name': dept['name']}
            )
            created_departments[dept['code']] = department
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {department.name}'))
            else:
                self.stdout.write(f'Department already exists: {department.name}')
        
        # Create courses
        courses = [
            {
                'title': 'Information Technology',
                'course_code': 'IT-301',
                'department': created_departments['TECH'],
                'icon_name': 'computer_outlined',
                'color_code': '#1E88E5',  # Colors.blue[600]
            },
            {
                'title': 'Business Administration',
                'course_code': 'BA-201',
                'department': created_departments['BUS'],
                'icon_name': 'business_center',
                'color_code': '#43A047',  # Colors.green[600]
            },
            {
                'title': 'Human Resources',
                'course_code': 'HR-220',
                'department': created_departments['BUS'],
                'icon_name': 'people_alt_outlined',
                'color_code': '#8E24AA',  # Colors.purple[600]
            },
            {
                'title': 'Maritime Studies',
                'course_code': 'MS-310',
                'department': created_departments['TRANS'],
                'icon_name': 'sailing_outlined',
                'color_code': '#1E88E5',  # Colors.blue[600]
            },
            {
                'title': 'Railway Engineering',
                'course_code': 'RE-250',
                'department': created_departments['TRANS'],
                'icon_name': 'train_outlined',
                'color_code': '#6D4C41',  # Colors.brown[600]
            },
            {
                'title': 'Mechanical Engineering',
                'course_code': 'ME-325',
                'department': created_departments['ENG'],
                'icon_name': 'precision_manufacturing_outlined',
                'color_code': '#F57C00',  # Colors.orange[600]
            },
            {
                'title': 'Automobile Engineering',
                'course_code': 'AE-340',
                'department': created_departments['ENG'],
                'icon_name': 'directions_car_outlined',
                'color_code': '#E53935',  # Colors.red[600]
            },
            {
                'title': 'Computer Science',
                'course_code': 'CS-301',
                'department': created_departments['TECH'],
                'icon_name': 'code_outlined',
                'color_code': '#3949AB',  # Colors.indigo[600]
            },
        ]
        
        for course_data in courses:
            course, created = Course.objects.get_or_create(
                course_code=course_data['course_code'],
                defaults={
                    'title': course_data['title'],
                    'department': course_data['department'],
                    'icon_name': course_data['icon_name'],
                    'color_code': course_data['color_code'],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
            else:
                self.stdout.write(f'Course already exists: {course.title}')
                
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully'))