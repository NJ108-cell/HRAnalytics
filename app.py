"""
Main Flask application for HR Analytics System
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Employee, PredictionHistory
from ml_engine import MLEngine
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize ML Engine
ml_engine = MLEngine()


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))


# ==================== Authentication Routes ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ==================== Dashboard Routes ====================

@app.route('/')
@login_required
def dashboard():
    """Main dashboard"""
    total_employees = Employee.query.count()
    
    # Department statistics
    dept_stats = db.session.query(
        Employee.department,
        db.func.count(Employee.id).label('count')
    ).group_by(Employee.department).all()
    
    # Recent predictions
    recent_predictions = PredictionHistory.query.order_by(
        PredictionHistory.timestamp.desc()
    ).limit(10).all()
    
    # Calculate average metrics
    avg_satisfaction = db.session.query(
        db.func.avg(Employee.job_satisfaction)
    ).scalar() or 0
    
    avg_work_life = db.session.query(
        db.func.avg(Employee.work_life_balance)
    ).scalar() or 0
    
    return render_template('dashboard.html',
                         total_employees=total_employees,
                         dept_stats=dept_stats,
                         recent_predictions=recent_predictions,
                         avg_satisfaction=round(avg_satisfaction, 2),
                         avg_work_life=round(avg_work_life, 2))


# ==================== Employee CRUD Routes ====================

@app.route('/employees')
@login_required
def employees():
    """List all employees"""
    page = request.args.get('page', 1, type=int)
    department = request.args.get('department', '')
    search = request.args.get('search', '')
    
    query = Employee.query
    
    if department:
        query = query.filter_by(department=department)
    
    if search:
        query = query.filter(Employee.name.contains(search))
    
    employees = query.order_by(Employee.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    departments = db.session.query(Employee.department).distinct().all()
    
    return render_template('employees.html',
                         employees=employees,
                         departments=[d[0] for d in departments],
                         current_department=department,
                         current_search=search)


@app.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """Add new employee"""
    if request.method == 'POST':
        try:
            employee = Employee(
                name=request.form.get('name'),
                age=int(request.form.get('age')),
                gender=request.form.get('gender'),
                department=request.form.get('department'),
                job_role=request.form.get('job_role'),
                salary=float(request.form.get('salary')),
                years_at_company=int(request.form.get('years_at_company')),
                job_satisfaction=int(request.form.get('job_satisfaction')),
                work_life_balance=int(request.form.get('work_life_balance')),
                performance_rating=int(request.form.get('performance_rating')),
                promotion_history=int(request.form.get('promotion_history')),
                overtime=request.form.get('overtime')
            )
            
            db.session.add(employee)
            db.session.commit()
            
            flash('Employee added successfully!', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'error')
    
    return render_template('add_employee.html')


@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """Edit employee"""
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            employee.name = request.form.get('name')
            employee.age = int(request.form.get('age'))
            employee.gender = request.form.get('gender')
            employee.department = request.form.get('department')
            employee.job_role = request.form.get('job_role')
            employee.salary = float(request.form.get('salary'))
            employee.years_at_company = int(request.form.get('years_at_company'))
            employee.job_satisfaction = int(request.form.get('job_satisfaction'))
            employee.work_life_balance = int(request.form.get('work_life_balance'))
            employee.performance_rating = int(request.form.get('performance_rating'))
            employee.promotion_history = int(request.form.get('promotion_history'))
            employee.overtime = request.form.get('overtime')
            
            db.session.commit()
            
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'error')
    
    return render_template('edit_employee.html', employee=employee)


@app.route('/employees/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    """Delete employee"""
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'error')
    
    return redirect(url_for('employees'))


# ==================== Analytics Routes ====================

@app.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard"""
    # Get all employees for analysis
    employees = Employee.query.all()
    
    # Department-wise attrition risk (if predictions exist)
    dept_risk = db.session.query(
        Employee.department,
        db.func.count(PredictionHistory.id).label('predictions'),
        db.func.avg(PredictionHistory.confidence_score).label('avg_risk')
    ).join(PredictionHistory).filter(
        PredictionHistory.prediction_type == 'Attrition'
    ).group_by(Employee.department).all()
    
    return render_template('analytics.html',
                         employees=employees,
                         dept_risk=dept_risk)


@app.route('/train-models', methods=['POST'])
@login_required
def train_models():
    """Train ML models"""
    try:
        # Get all employees
        employees = Employee.query.all()
        
        if len(employees) < 10:
            return jsonify({
                'success': False,
                'message': 'Need at least 10 employees to train models'
            })
        
        # Convert to DataFrame
        data = pd.DataFrame([emp.to_dict() for emp in employees])
        data = data.drop(columns=['id'])  # Remove ID column
        
        # Train models
        attrition_metrics = ml_engine.train_attrition_model(data)
        performance_metrics = ml_engine.train_performance_model(data)
        
        return jsonify({
            'success': True,
            'message': 'Models trained successfully!',
            'attrition_metrics': attrition_metrics,
            'performance_metrics': performance_metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error training models: {str(e)}'
        })


@app.route('/predict/<int:employee_id>', methods=['POST'])
@login_required
def predict_employee(employee_id):
    """Run predictions for a specific employee"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        # Load models if not already loaded
        if ml_engine.attrition_model is None or ml_engine.performance_model is None:
            ml_engine.load_models()
        
        # Get employee data
        employee_data = employee.to_dict()
        
        # Make predictions
        attrition_pred = ml_engine.predict_attrition(employee_data)
        performance_pred = ml_engine.predict_performance(employee_data)
        
        # Save predictions to history
        attrition_history = PredictionHistory(
            employee_id=employee.id,
            prediction_type='Attrition',
            result=attrition_pred['result'],
            confidence_score=attrition_pred['risk_score']
        )
        
        performance_history = PredictionHistory(
            employee_id=employee.id,
            prediction_type='Performance',
            result=performance_pred['result'],
            confidence_score=performance_pred['confidence']
        )
        
        db.session.add(attrition_history)
        db.session.add(performance_history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attrition': attrition_pred,
            'performance': performance_pred
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


@app.route('/predict-all', methods=['POST'])
@login_required
def predict_all():
    """Run predictions for all employees"""
    try:
        # Load models
        if ml_engine.attrition_model is None or ml_engine.performance_model is None:
            ml_engine.load_models()
        
        employees = Employee.query.all()
        predictions_made = 0
        
        for employee in employees:
            employee_data = employee.to_dict()
            
            # Make predictions
            attrition_pred = ml_engine.predict_attrition(employee_data)
            performance_pred = ml_engine.predict_performance(employee_data)
            
            # Save to history
            attrition_history = PredictionHistory(
                employee_id=employee.id,
                prediction_type='Attrition',
                result=attrition_pred['result'],
                confidence_score=attrition_pred['risk_score']
            )
            
            performance_history = PredictionHistory(
                employee_id=employee.id,
                prediction_type='Performance',
                result=performance_pred['result'],
                confidence_score=performance_pred['confidence']
            )
            
            db.session.add(attrition_history)
            db.session.add(performance_history)
            predictions_made += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Predictions completed for {predictions_made} employees'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        })


@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    # Attrition rate by department
    dept_attrition = db.session.query(
        Employee.department,
        db.func.count(PredictionHistory.id).label('total_predictions'),
        db.func.sum(
            db.case((PredictionHistory.result == 'Leave', 1), else_=0)
        ).label('leave_count')
    ).join(PredictionHistory).filter(
        PredictionHistory.prediction_type == 'Attrition'
    ).group_by(Employee.department).all()
    
    # Recent predictions
    recent_predictions = PredictionHistory.query.order_by(
        PredictionHistory.timestamp.desc()
    ).limit(50).all()
    
    return render_template('reports.html',
                         dept_attrition=dept_attrition,
                         recent_predictions=recent_predictions)


# ==================== API Routes ====================

@app.route('/api/employees', methods=['GET'])
@login_required
def api_get_employees():
    """API: Get all employees"""
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])


@app.route('/api/employees/<int:id>', methods=['GET'])
@login_required
def api_get_employee(id):
    """API: Get specific employee"""
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
