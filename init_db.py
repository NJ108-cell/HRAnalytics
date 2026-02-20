"""
Database initialization script with dummy data
"""
import random
from models import db, User, Employee
from datetime import datetime


def init_database(app):
    """Initialize database with tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


def create_dummy_data(app):
    """Create dummy data for testing"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Define departments and job roles
        departments = {
            'Sales': ['Sales Executive', 'Sales Manager', 'Account Manager', 'Sales Representative'],
            'Engineering': ['Software Engineer', 'Senior Engineer', 'Tech Lead', 'DevOps Engineer'],
            'HR': ['HR Manager', 'Recruiter', 'HR Coordinator', 'Training Specialist'],
            'Marketing': ['Marketing Manager', 'Content Writer', 'SEO Specialist', 'Brand Manager'],
            'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'Controller'],
            'Operations': ['Operations Manager', 'Project Manager', 'Business Analyst', 'Operations Coordinator']
        }
        
        # Generate employee names
        first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'James', 'Lisa',
                      'Robert', 'Jennifer', 'William', 'Amanda', 'Christopher', 'Ashley', 'Daniel',
                      'Stephanie', 'Matthew', 'Nicole', 'Anthony', 'Elizabeth', 'Mark', 'Heather',
                      'Donald', 'Michelle', 'Steven', 'Kimberly', 'Paul', 'Amy', 'Andrew', 'Melissa']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                     'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White',
                     'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker']
        
        genders = ['Male', 'Female']
        overtime_options = ['Yes', 'No']
        
        # Create 150 dummy employees
        employees = []
        for i in range(150):
            dept = random.choice(list(departments.keys()))
            role = random.choice(departments[dept])
            
            # Generate realistic salary based on department and role
            base_salary = {
                'Sales': 55000,
                'Engineering': 75000,
                'HR': 50000,
                'Marketing': 60000,
                'Finance': 70000,
                'Operations': 65000
            }
            
            salary = base_salary[dept] + random.randint(-10000, 40000)
            
            # Generate correlated attributes
            years = random.randint(0, 15)
            age = random.randint(22, 60)
            
            # Satisfaction tends to be higher with promotions
            promotions = min(years // 3, random.randint(0, 5))
            satisfaction = random.randint(1, 5)
            if promotions > 2:
                satisfaction = min(5, satisfaction + 1)
            
            # Work-life balance affected by overtime
            overtime = random.choice(overtime_options)
            work_life = random.randint(1, 5)
            if overtime == 'Yes':
                work_life = max(1, work_life - 1)
            
            employee = Employee(
                name=f"{random.choice(first_names)} {random.choice(last_names)}",
                age=age,
                gender=random.choice(genders),
                department=dept,
                job_role=role,
                salary=salary,
                years_at_company=years,
                job_satisfaction=satisfaction,
                work_life_balance=work_life,
                performance_rating=random.randint(1, 3),
                promotion_history=promotions,
                overtime=overtime
            )
            employees.append(employee)
        
        # Add all employees to session
        db.session.bulk_save_objects(employees)
        
        # Commit all changes
        db.session.commit()
        
        print(f"Created admin user (username: admin, password: admin123)")
        print(f"Created {len(employees)} dummy employees")
        print("Database initialization complete!")


def get_database_stats(app):
    """Get statistics about the database"""
    with app.app_context():
        total_employees = Employee.query.count()
        dept_stats = db.session.query(
            Employee.department,
            db.func.count(Employee.id)
        ).group_by(Employee.department).all()
        
        print(f"\n{'='*50}")
        print(f"DATABASE STATISTICS")
        print(f"{'='*50}")
        print(f"Total Employees: {total_employees}")
        print(f"\nEmployees by Department:")
        for dept, count in dept_stats:
            print(f"  {dept}: {count}")
        print(f"{'='*50}\n")
