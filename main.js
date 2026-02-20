// Main JavaScript for HR Analytics System

// Show loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Train models
function trainModels() {
    if (!confirm('This will train both Attrition and Performance models. Continue?')) {
        return;
    }
    
    showLoading();
    
    fetch('/train-models', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            alert('Models trained successfully!\n\n' +
                  'Attrition Model Accuracy: ' + (data.attrition_metrics.accuracy * 100).toFixed(2) + '%\n' +
                  'Performance Model Accuracy: ' + (data.performance_metrics.accuracy * 100).toFixed(2) + '%');
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        hideLoading();
        alert('Error training models: ' + error);
    });
}

// Predict for single employee
function predictEmployee(employeeId) {
    showLoading();
    
    fetch(`/predict/${employeeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            const attrition = data.attrition;
            const performance = data.performance;
            
            alert('Prediction Results:\n\n' +
                  'Attrition Risk: ' + attrition.result + ' (' + attrition.risk_score + '%)\n' +
                  'Performance Level: ' + performance.result + ' (' + performance.confidence + '% confidence)');
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        hideLoading();
        alert('Error making prediction: ' + error);
    });
}

// Predict for all employees
function predictAll() {
    if (!confirm('This will run predictions for all employees. This may take a while. Continue?')) {
        return;
    }
    
    showLoading();
    
    fetch('/predict-all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        hideLoading();
        alert('Error making predictions: ' + error);
    });
}

// Delete employee with confirmation
function deleteEmployee(employeeId, employeeName) {
    if (confirm(`Are you sure you want to delete ${employeeName}? This action cannot be undone.`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/employees/delete/${employeeId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Add slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
function validateEmployeeForm() {
    const age = parseInt(document.getElementById('age').value);
    const salary = parseFloat(document.getElementById('salary').value);
    const years = parseInt(document.getElementById('years_at_company').value);
    
    if (age < 18 || age > 100) {
        alert('Age must be between 18 and 100');
        return false;
    }
    
    if (salary < 0) {
        alert('Salary must be a positive number');
        return false;
    }
    
    if (years < 0) {
        alert('Years at company cannot be negative');
        return false;
    }
    
    return true;
}
