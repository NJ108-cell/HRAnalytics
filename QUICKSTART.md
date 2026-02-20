# 🚀 Quick Start Guide - HR Analytics System

## Installation (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Application
```bash
python run.py
```

When prompted "Would you like to create dummy data for testing?", type **yes**

### 3️⃣ Access the System
Open your browser and go to: **http://localhost:5000**

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

---

## First Time Setup (5 Minutes)

### Step 1: Login
Use the default credentials above to login.

### Step 2: Explore Employees
- Click **"Employees"** in the sidebar
- Browse the 150 dummy employees created
- Try searching or filtering by department

### Step 3: Train ML Models
- Click **"ML Analytics"** in the sidebar
- Click the **"Train Models"** button
- Wait for the success message (shows accuracy metrics)

### Step 4: Run Predictions
- On the same ML Analytics page
- Click **"Predict All"** button
- This will predict attrition risk and performance for all employees

### Step 5: View Results
- Click **"Dashboard"** to see overview
- Click **"Reports"** to see detailed analytics
- Check department-wise attrition rates
- Review prediction history

---

## Key Features to Try

### ✅ Employee Management
- **Add Employee**: Click "Add Employee" button on Employees page
- **Edit Employee**: Click edit icon (pencil) next to any employee
- **Delete Employee**: Click delete icon (trash) - confirms before deleting
- **Search**: Use the search bar to find employees by name
- **Filter**: Filter by department using the dropdown

### 🤖 ML Predictions
- **Single Prediction**: Click brain icon next to any employee
- **Bulk Prediction**: Use "Predict All" on ML Analytics page
- **View Results**: Check Dashboard or Reports page

### 📊 Analytics & Reports
- **Dashboard**: Overview of all metrics
- **Department Statistics**: See employee distribution
- **Attrition Analysis**: Department-wise risk scores
- **Prediction History**: Complete audit trail

---

## Common Tasks

### How to Add a New Employee
1. Click "Employees" → "Add Employee"
2. Fill in all required fields (marked with *)
3. Click "Save Employee"
4. Employee appears in the list immediately

### How to Train Models
1. Go to "ML Analytics"
2. Click "Train Models"
3. Wait for completion (shows accuracy)
4. Models are now ready for predictions

### How to Predict Attrition Risk
**For one employee:**
- Go to "Employees"
- Click brain icon next to employee
- See results in popup

**For all employees:**
- Go to "ML Analytics"
- Click "Predict All"
- Check "Reports" for results

### How to View Department Risk
1. Click "Reports" in sidebar
2. See "Department Attrition Analysis" table
3. Green = Low Risk, Yellow = Warning, Red = Critical

---

## Understanding the Results

### Attrition Prediction
- **Stay**: Employee likely to remain (Low risk)
- **Leave**: Employee at risk of leaving (High risk)
- **Risk Score**: 0-100% probability of leaving

### Performance Prediction
- **High**: Top performer (Rating 3)
- **Medium**: Average performer (Rating 2)
- **Low**: Needs improvement (Rating 1)
- **Confidence**: How confident the model is (%)

---

## Tips & Best Practices

1. **Train Regularly**: Retrain models when you add new employees
2. **Check Reports**: Review department risk weekly
3. **Act on Insights**: Take action on high-risk employees
4. **Keep Data Updated**: Update employee records regularly
5. **Monitor Trends**: Track attrition rates over time

---

## Troubleshooting

**Issue**: Can't login
- **Solution**: Use username: `admin`, password: `admin123`

**Issue**: "Models not trained" error
- **Solution**: Go to ML Analytics → Click "Train Models"

**Issue**: No predictions showing
- **Solution**: Train models first, then run "Predict All"

**Issue**: Page not loading
- **Solution**: Check if server is running on http://localhost:5000

---

## Next Steps

After completing the quick start:
1. Read the full README.md for detailed documentation
2. Explore the code structure in different modules
3. Try the API endpoints for integration
4. Customize the system for your needs

---

## System Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 500MB free disk space
- Internet connection (for initial setup only)

---

**Need Help?** Check the README.md file for comprehensive documentation.

**Ready to Deploy?** Review the Configuration section in README.md.
