"""
Database models for HR Analytics System
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Employee(db.Model):
    """Employee model with all HR-related fields"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    years_at_company = db.Column(db.Integer, nullable=False)
    job_satisfaction = db.Column(db.Integer, nullable=False)  # 1-5
    work_life_balance = db.Column(db.Integer, nullable=False)  # 1-5
    performance_rating = db.Column(db.Integer, nullable=False)  # 1-3
    promotion_history = db.Column(db.Integer, default=0)  # Number of promotions
    overtime = db.Column(db.String(3), nullable=False)  # Yes/No
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    predictions = db.relationship('PredictionHistory', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert employee to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'department': self.department,
            'job_role': self.job_role,
            'salary': self.salary,
            'years_at_company': self.years_at_company,
            'job_satisfaction': self.job_satisfaction,
            'work_life_balance': self.work_life_balance,
            'performance_rating': self.performance_rating,
            'promotion_history': self.promotion_history,
            'overtime': self.overtime
        }
    
    def __repr__(self):
        return f'<Employee {self.name} - {self.department}>'


class PredictionHistory(db.Model):
    """Prediction history for audit trail"""
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    prediction_type = db.Column(db.String(20), nullable=False)  # Attrition/Performance
    result = db.Column(db.String(50), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else 'Unknown',
            'prediction_type': self.prediction_type,
            'result': self.result,
            'confidence_score': round(self.confidence_score, 2),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Prediction {self.prediction_type} - {self.result}>'
