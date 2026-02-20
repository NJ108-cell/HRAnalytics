# HR Analytics System

A comprehensive, production-ready HR Analytics platform powered by Machine Learning that predicts employee attrition risk and performance levels using Random Forest algorithms.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.2-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Functionality
- **Employee Management**: Complete CRUD operations for employee records
- **ML-Powered Predictions**: 
  - Attrition Risk Prediction (Stay/Leave with confidence %)
  - Performance Level Classification (Low/Medium/High)
- **Real-time Analytics**: Interactive dashboards with department-wise insights
- **Audit Trail**: Complete prediction history for compliance and analysis
- **User Authentication**: Secure login system with hashed passwords

### Technical Highlights
- **Modern UI**: Responsive, professional design with dark theme
- **RESTful API**: Clean API endpoints for integration
- **Data Preprocessing**: Automated feature scaling and encoding
- **Model Persistence**: Trained models saved for quick predictions
- **Scalable Architecture**: Modular design following best practices

## 🏗️ Project Structure

```
hr_analytics_system/
├── app.py                  # Main Flask application
├── models.py              # Database models (SQLAlchemy)
├── ml_engine.py           # Machine Learning engine
├── preprocessing.py       # Data preprocessing module
├── init_db.py            # Database initialization
├── run.py                # Application launcher
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Modern CSS styling
│   └── js/
│       └── main.js      # JavaScript functions
├── templates/
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard
│   ├── employees.html   # Employee listing
│   ├── add_employee.html
│   ├── edit_employee.html
│   ├── analytics.html   # ML analytics page
│   └── reports.html     # Reports and insights
└── models/              # Saved ML models (created at runtime)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone or extract the project**
```bash
cd hr_analytics_system
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python run.py
```

The script will:
- Create the database (if it doesn't exist)
- Offer to generate dummy data for testing
- Start the Flask development server

5. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

**Default Login Credentials:**
- Username: `admin`
- Password: `admin123`

## 📊 Database Schema

### Employees Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String(100) | Full name |
| age | Integer | Employee age |
| gender | String(20) | Gender |
| department | String(50) | Department name |
| job_role | String(100) | Job title |
| salary | Float | Annual salary |
| years_at_company | Integer | Tenure |
| job_satisfaction | Integer | 1-5 scale |
| work_life_balance | Integer | 1-5 scale |
| performance_rating | Integer | 1-3 (Low/Medium/High) |
| promotion_history | Integer | Number of promotions |
| overtime | String(3) | Yes/No |

### PredictionHistory Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| employee_id | Integer | Foreign key to Employee |
| prediction_type | String(20) | Attrition/Performance |
| result | String(50) | Prediction result |
| confidence_score | Float | Confidence percentage |
| timestamp | DateTime | When prediction was made |

### Users Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String(80) | Unique username |
| password_hash | String(255) | Hashed password |

## 🤖 Machine Learning Engine

### Attrition Prediction Model
- **Algorithm**: Random Forest Classifier
- **Features**: All employee attributes
- **Output**: 
  - Binary classification (Stay/Leave)
  - Risk score (0-100%)
  - Confidence level

### Performance Prediction Model
- **Algorithm**: Random Forest Classifier
- **Features**: Employee attributes (excluding performance_rating)
- **Output**:
  - Multi-class (Low/Medium/High)
  - Confidence percentage

### Data Preprocessing
1. **Missing Value Handling**:
   - Numerical: Median imputation
   - Categorical: Mode imputation

2. **Feature Engineering**:
   - Label encoding for categorical variables
   - Standard scaling for numerical features

3. **Model Training**:
   - 80/20 train-test split
   - Cross-validation ready
   - Hyperparameter optimization

## 🎯 Usage Guide

### 1. Employee Management
- **Add Employee**: Click "Add Employee" button → Fill form → Save
- **Edit Employee**: Click edit icon → Modify fields → Update
- **Delete Employee**: Click delete icon → Confirm deletion
- **Search/Filter**: Use search bar and department filter

### 2. Training ML Models
1. Navigate to "ML Analytics" page
2. Click "Train Models" button
3. System will:
   - Preprocess all employee data
   - Train Attrition model
   - Train Performance model
   - Display accuracy metrics

### 3. Making Predictions
**Single Employee:**
- From Employees page, click brain icon next to employee
- View prediction results in popup

**All Employees:**
- Go to ML Analytics page
- Click "Predict All" button
- System processes all employees

### 4. Viewing Reports
- **Dashboard**: Overview metrics and recent predictions
- **Reports**: Department-wise attrition analysis
- **Prediction History**: Audit trail of all predictions

## 🔌 API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout user

### Dashboard
- `GET /` - Main dashboard

### Employee CRUD
- `GET /employees` - List employees (with pagination/filtering)
- `GET /employees/add` - Add employee form
- `POST /employees/add` - Create new employee
- `GET /employees/edit/<id>` - Edit employee form
- `POST /employees/edit/<id>` - Update employee
- `POST /employees/delete/<id>` - Delete employee

### Analytics
- `GET /analytics` - ML analytics page
- `POST /train-models` - Train ML models
- `POST /predict/<employee_id>` - Predict for single employee
- `POST /predict-all` - Predict for all employees
- `GET /reports` - View reports

### API (JSON)
- `GET /api/employees` - Get all employees as JSON
- `GET /api/employees/<id>` - Get specific employee as JSON

## 🎨 UI Features

### Design Elements
- **Dark Theme**: Professional dark interface with gradient accents
- **Responsive**: Works on desktop, tablet, and mobile
- **Modern Typography**: Space Grotesk & Inter fonts
- **Smooth Animations**: CSS transitions and hover effects
- **Color Coding**: Visual indicators for risk levels and performance

### User Experience
- **Flash Messages**: Auto-dismissing notifications
- **Loading Overlays**: Visual feedback during processing
- **Pagination**: Efficient browsing of large datasets
- **Form Validation**: Client and server-side validation
- **Confirmation Dialogs**: Prevent accidental deletions

## 📈 Model Performance

The ML models are evaluated using:
- **Accuracy Score**: Overall prediction accuracy
- **Confusion Matrix**: Detailed classification results
- **Classification Report**: Precision, recall, F1-score

Metrics are displayed when models are trained.

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hr_analytics.db
FLASK_ENV=production
```

### Database Configuration
By default, uses SQLite database (`hr_analytics.db`). To use PostgreSQL or MySQL:

1. Update `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

2. Install appropriate driver:
```bash
pip install psycopg2-binary  # For PostgreSQL
# or
pip install pymysql  # For MySQL
```

## 🛠️ Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database not found
**Solution**: Run the initialization script
```bash
python run.py
```

### Issue: Models not trained
**Solution**: Navigate to ML Analytics and click "Train Models"

### Issue: Low prediction accuracy
**Solution**: 
- Add more employee data
- Ensure data quality
- Retrain models with updated data

## 📝 Code Quality

- **PEP 8 Compliant**: Follows Python style guidelines
- **Modular Design**: Separation of concerns
- **Comprehensive Comments**: Well-documented code
- **Error Handling**: Try-catch blocks for robustness
- **Type Hints**: (Can be added for enhanced IDE support)

## 🚀 Future Enhancements

Potential improvements:
- [ ] Advanced visualizations (charts/graphs)
- [ ] Export reports to PDF/Excel
- [ ] Email notifications for high-risk employees
- [ ] Role-based access control (Admin/Manager/Viewer)
- [ ] Batch employee upload (CSV import)
- [ ] Model comparison and A/B testing
- [ ] Real-time dashboard updates
- [ ] Integration with external HR systems

## 📄 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Technical Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy ORM with SQLite
- **ML**: Scikit-learn 1.3.2
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Authentication**: Flask-Login
- **Security**: Werkzeug password hashing

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review code comments and documentation
3. Examine error logs in console

## 🎉 Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python run.py

# 3. Open browser
http://localhost:5000

# 4. Login
Username: admin
Password: admin123

# 5. Train models
Go to ML Analytics → Train Models

# 6. Make predictions
Click "Predict All" or predict individual employees
```

---

**Built with ❤️ using Python, Flask, and Machine Learning**
