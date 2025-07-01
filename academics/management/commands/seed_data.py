from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from academics.models import Course, Department, CourseNote


User = get_user_model()

#allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png']
class Command(BaseCommand):
    help = 'Seeds the database with initial departments, courses, and sample notes'

    def handle(self, *args, **kwargs):
        # Create superuser with EMAIL and PASSWORD only
        admin_user, created = User.objects.get_or_create(
            email='admin@esterMollel.com',
            defaults={'password': 'esterMollel2001'}
        )
        if created:
            admin_user.set_password('esterMollel2001')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write('Superuser already exists')
        
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
                'module_code': 'IT-301',
                'department': created_departments['TECH'],
                'icon_name': 'computer_outlined',
                'color_code': '#1E88E5',  # Colors.blue[600]
            },
            {
                'title': 'Business Administration',
                'module_code': 'BA-201',
                'department': created_departments['BUS'],
                'icon_name': 'business_center',
                'color_code': '#43A047',  # Colors.green[600]
            },
            {
                'title': 'Human Resources',
                'module_code': 'HR-220',
                'department': created_departments['BUS'],
                'icon_name': 'people_alt_outlined',
                'color_code': '#8E24AA',  # Colors.purple[600]
            },
            {
                'title': 'Maritime Studies',
                'module_code': 'MS-310',
                'department': created_departments['TRANS'],
                'icon_name': 'sailing_outlined',
                'color_code': '#1E88E5',  # Colors.blue[600]
            },
            {
                'title': 'Railway Engineering',
                'module_code': 'RE-250',
                'department': created_departments['TRANS'],
                'icon_name': 'train_outlined',
                'color_code': '#6D4C41',  # Colors.brown[600]
            },
            {
                'title': 'Mechanical Engineering',
                'module_code': 'ME-325',
                'department': created_departments['ENG'],
                'icon_name': 'precision_manufacturing_outlined',
                'color_code': '#F57C00',  # Colors.orange[600]
            },
            {
                'title': 'Automobile Engineering',
                'module_code': 'AE-340',
                'department': created_departments['ENG'],
                'icon_name': 'directions_car_outlined',
                'color_code': '#E53935',  # Colors.red[600]
            },
            {
                'title': 'Computer Science',
                'module_code': 'CS-301',
                'department': created_departments['TECH'],
                'icon_name': 'code_outlined',
                'color_code': '#3949AB',  # Colors.indigo[600]
            },
        ]
        
        created_courses = {}
        for course_data in courses:
            course, created = Course.objects.get_or_create(
                module_code=course_data['module_code'],
                defaults={
                    'title': course_data['title'],
                    'department': course_data['department'],
                    'icon_name': course_data['icon_name'],
                    'color_code': course_data['color_code'],
                }
            )
            created_courses[course_data['module_code']] = course
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
            else:
                self.stdout.write(f'Course already exists: {course.title}')
        
        # Create sample course notes
        sample_notes = [
            # Information Technology Notes
            {
                'title': 'Introduction to Python Programming',
                'course': created_courses['IT-301'],
                'category': 'lecture',
                'difficulty_level': 'beginner',
                'content': '''Python is a high-level, interpreted programming language known for its simplicity and readability. 

Key Features:
- Easy to learn and use
- Interpreted language (no compilation needed)
- Object-oriented programming support
- Large standard library
- Cross-platform compatibility

Basic Syntax:
Python uses indentation to define code blocks instead of braces. This makes the code more readable and enforces good programming practices.

Variables in Python:
Variables are created when you assign a value to them. Python is dynamically typed, meaning you don't need to declare variable types.

Example:
name = "John"
age = 25
height = 5.9

Print Statement:
The print() function is used to display output to the console.

Example:
print("Hello, World!")
print(f"My name is {name} and I am {age} years old")''',
                'tags': 'python, programming, basics, syntax',
                'is_featured': True,
                'order': 1,
                'chapter': 'Chapter 1: Python Fundamentals',
            },
            {
                'title': 'Python Data Types and Variables',
                'course': created_courses['IT-301'],
                'category': 'concept',
                'difficulty_level': 'beginner',
                'content': '''Python supports several built-in data types that are essential for programming.

Numeric Types:
1. int - Integer numbers (e.g., 42, -17, 0)
2. float - Decimal numbers (e.g., 3.14, -2.5, 0.0)
3. complex - Complex numbers (e.g., 3+4j)

Text Type:
str - String (e.g., "Hello", 'Python', "123")

Boolean Type:
bool - True or False values

Sequence Types:
1. list - Ordered, mutable collection [1, 2, 3]
2. tuple - Ordered, immutable collection (1, 2, 3)
3. range - Sequence of numbers range(0, 10)

Mapping Type:
dict - Key-value pairs {"name": "John", "age": 25}

Set Types:
1. set - Unordered collection of unique items {1, 2, 3}
2. frozenset - Immutable set

Variable Assignment:
Variables are created by assignment and can hold any data type.

Examples:
number = 42
name = "Alice"
is_student = True
grades = [85, 92, 78, 96]
person = {"name": "Bob", "age": 30}''',
                'tags': 'python, data types, variables, basics',
                'order': 2,
                'chapter': 'Chapter 1: Python Fundamentals',
            },
            
            # Computer Science Notes
            {
                'title': 'Algorithms and Data Structures Overview',
                'course': created_courses['CS-301'],
                'category': 'lecture',
                'difficulty_level': 'intermediate',
                'content': '''Algorithms and Data Structures form the foundation of computer science and efficient programming.

What is an Algorithm?
An algorithm is a step-by-step procedure for solving a problem or completing a task. Good algorithms are:
- Correct: Produces the right output for all valid inputs
- Efficient: Uses minimal time and space resources
- Clear: Easy to understand and implement

Common Algorithm Categories:
1. Sorting Algorithms (Bubble Sort, Quick Sort, Merge Sort)
2. Searching Algorithms (Linear Search, Binary Search)
3. Graph Algorithms (DFS, BFS, Dijkstra's)
4. Dynamic Programming
5. Greedy Algorithms

What are Data Structures?
Data structures are ways of organizing and storing data to enable efficient access and modification.

Linear Data Structures:
- Arrays: Fixed-size sequential collection
- Linked Lists: Dynamic sequential collection
- Stacks: LIFO (Last In, First Out)
- Queues: FIFO (First In, First Out)

Non-Linear Data Structures:
- Trees: Hierarchical structure
- Graphs: Network of connected nodes
- Hash Tables: Key-value mapping

Algorithm Complexity:
We measure algorithm efficiency using Big O notation:
- O(1): Constant time
- O(log n): Logarithmic time
- O(n): Linear time
- O(n²): Quadratic time''',
                'tags': 'algorithms, data structures, complexity, big o',
                'is_featured': True,
                'order': 1,
                'chapter': 'Chapter 1: Fundamentals',
            },
            
            # Business Administration Notes
            {
                'title': 'Principles of Management',
                'course': created_courses['BA-201'],
                'category': 'lecture',
                'difficulty_level': 'beginner',
                'content': '''Management is the process of planning, organizing, leading, and controlling organizational resources to achieve specific goals.

The Four Functions of Management:

1. Planning
- Setting objectives and goals
- Developing strategies and action plans
- Forecasting future needs and challenges
- Decision making about resource allocation

2. Organizing
- Structuring the organization
- Assigning roles and responsibilities
- Creating reporting relationships
- Coordinating activities and resources

3. Leading
- Motivating employees
- Communicating vision and goals
- Resolving conflicts
- Building team relationships

4. Controlling
- Monitoring performance
- Comparing actual results with planned results
- Taking corrective action when needed
- Establishing performance standards

Management Levels:
- Top Management: CEO, President, VP (Strategic decisions)
- Middle Management: Department heads, Division managers (Tactical decisions)
- First-line Management: Supervisors, Team leaders (Operational decisions)

Key Management Skills:
- Technical Skills: Job-specific knowledge and expertise
- Human Relations Skills: Ability to work with people
- Conceptual Skills: Ability to see the big picture

Modern Management Challenges:
- Globalization
- Technology advancement
- Workforce diversity
- Environmental sustainability
- Ethical considerations''',
                'tags': 'management, planning, organizing, leading, controlling',
                'is_featured': True,
                'order': 1,
                'chapter': 'Chapter 1: Management Fundamentals',
            },
            
            # Human Resources Notes
            {
                'title': 'Introduction to Human Resource Management',
                'course': created_courses['HR-220'],
                'category': 'lecture',
                'difficulty_level': 'beginner',
                'content': '''Human Resource Management (HRM) is the strategic approach to managing an organization's most valuable assets - its people.

What is HRM?
HRM involves recruiting, hiring, deploying, and managing employees to help achieve organizational objectives while ensuring employee satisfaction and legal compliance.

Core HRM Functions:

1. Human Resource Planning
- Forecasting future staffing needs
- Analyzing current workforce capabilities
- Developing strategies to meet future needs

2. Recruitment and Selection
- Attracting qualified candidates
- Screening and interviewing applicants
- Making hiring decisions

3. Training and Development
- Onboarding new employees
- Providing skills training
- Career development programs
- Leadership development

4. Performance Management
- Setting performance standards
- Conducting performance appraisals
- Providing feedback and coaching
- Managing underperformance

5. Compensation and Benefits
- Designing salary structures
- Managing employee benefits
- Incentive programs
- Ensuring pay equity

6. Employee Relations
- Maintaining positive workplace relationships
- Handling grievances and conflicts
- Employee engagement initiatives
- Union relations (if applicable)

7. Legal Compliance
- Employment law compliance
- Workplace safety regulations
- Anti-discrimination policies
- Record keeping requirements

Strategic Importance of HRM:
- Competitive advantage through people
- Organizational culture development
- Change management
- Talent retention
- Productivity improvement''',
                'tags': 'human resources, HRM, recruitment, training, performance',
                'is_featured': True,
                'order': 1,
                'chapter': 'Chapter 1: HRM Fundamentals',
            },
            
            # Mechanical Engineering Notes
            {
                'title': 'Fundamentals of Thermodynamics',
                'course': created_courses['ME-325'],
                'category': 'lecture',
                'difficulty_level': 'intermediate',
                'content': '''Thermodynamics is the branch of physics that deals with heat, work, temperature, and energy.

Basic Concepts:

System: The part of the universe being studied
Surroundings: Everything outside the system
Boundary: The interface between system and surroundings

Types of Systems:
1. Open System: Mass and energy can cross boundaries
2. Closed System: Only energy can cross boundaries
3. Isolated System: Neither mass nor energy can cross boundaries

Properties:
- Intensive Properties: Independent of mass (temperature, pressure)
- Extensive Properties: Dependent on mass (volume, internal energy)

State Functions: Properties that depend only on current state
- Temperature (T)
- Pressure (P)
- Volume (V)
- Internal Energy (U)
- Enthalpy (H)
- Entropy (S)

The Four Laws of Thermodynamics:

Zeroth Law: If two systems are in thermal equilibrium with a third, they are in thermal equilibrium with each other.

First Law: Energy cannot be created or destroyed, only converted from one form to another.
ΔU = Q - W
Where: ΔU = change in internal energy, Q = heat added, W = work done by system

Second Law: The entropy of an isolated system never decreases.
Heat flows spontaneously from hot to cold bodies.

Third Law: The entropy of a perfect crystal approaches zero as temperature approaches absolute zero.

Applications:
- Heat engines
- Refrigeration systems
- Power plants
- HVAC systems''',
                'tags': 'thermodynamics, energy, heat, work, laws',
                'order': 1,
                'chapter': 'Chapter 1: Basic Thermodynamics',
            },
            
            # Tutorial and Assignment Examples
            {
                'title': 'Python Programming Exercise: Loops and Conditionals',
                'course': created_courses['IT-301'],
                'category': 'tutorial',
                'difficulty_level': 'beginner',
                'content': '''Practice exercises for Python loops and conditional statements.

Exercise 1: Number Guessing Game
Write a program that:
1. Generates a random number between 1 and 100
2. Asks the user to guess the number
3. Provides hints (too high/too low)
4. Counts the number of attempts

Exercise 2: Grade Calculator
Create a program that:
1. Asks for student scores in 5 subjects
2. Calculates the average
3. Assigns letter grades based on average:
   - A: 90-100
   - B: 80-89
   - C: 70-79
   - D: 60-69
   - F: Below 60

Exercise 3: Multiplication Table
Write a program that prints multiplication tables from 1 to 10 using nested loops.

Exercise 4: Prime Number Checker
Create a function that checks if a given number is prime.

Tips for Success:
- Test your code with different inputs
- Use meaningful variable names
- Add comments to explain complex logic
- Handle edge cases (invalid inputs)
- Practice debugging techniques

Submission Guidelines:
- Submit well-commented code
- Include test cases with outputs
- Explain your approach for each solution''',
                'tags': 'python, exercises, loops, conditionals, practice',
                'order': 3,
                'chapter': 'Chapter 2: Control Structures',
            },
            
            # Exam Preparation
            {
                'title': 'Final Exam Preparation - Business Administration',
                'course': created_courses['BA-201'],
                'category': 'exam_prep',
                'difficulty_level': 'intermediate',
                'content': '''Comprehensive review guide for the Business Administration final exam.

Exam Format:
- Duration: 3 hours
- Multiple Choice: 50 questions (50 points)
- Short Answers: 5 questions (25 points)
- Essay Questions: 2 questions (25 points)

Key Topics to Review:

1. Management Functions (20% of exam)
- Planning, organizing, leading, controlling
- Management levels and skills
- Decision-making processes

2. Organizational Behavior (25% of exam)
- Motivation theories
- Leadership styles
- Team dynamics
- Communication

3. Marketing Fundamentals (20% of exam)
- Marketing mix (4Ps)
- Market segmentation
- Consumer behavior
- Brand management

4. Financial Management (20% of exam)
- Financial statements
- Budgeting and forecasting
- Investment decisions
- Risk management

5. Operations Management (15% of exam)
- Production planning
- Quality control
- Supply chain management
- Process improvement

Study Tips:
- Review all lecture notes and textbook chapters
- Practice with past exam questions
- Form study groups for discussion
- Create concept maps for complex topics
- Focus on understanding concepts, not just memorization

Important Formulas:
- Break-even Point = Fixed Costs / (Price - Variable Cost)
- ROI = (Gain - Cost) / Cost × 100
- Current Ratio = Current Assets / Current Liabilities

Sample Essay Questions:
1. Discuss the evolution of management theories and their relevance today
2. Analyze the impact of digital transformation on modern business practices''',
                'tags': 'exam, review, business administration, study guide',
                'is_featured': True,
                'order': 10,
                'chapter': 'Final Review',
            },
        ]
        
        # Create the notes
        for note_data in sample_notes:
            note, created = CourseNote.objects.get_or_create(
                title=note_data['title'],
                course=note_data['course'],
                defaults={
                    'category': note_data['category'],
                    'difficulty_level': note_data['difficulty_level'],
                    'content': note_data['content'],
                    'tags': note_data['tags'],
                    'is_featured': note_data.get('is_featured', False),
                    'order': note_data['order'],
                    'chapter': note_data.get('chapter'),
                    'created_by': admin_user,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created note: {note.title}'))
            else:
                self.stdout.write(f'Note already exists: {note.title}')
                
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully'))
        self.stdout.write(f'Created {CourseNote.objects.count()} course notes in total')