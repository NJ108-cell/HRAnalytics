"""
Machine Learning Engine for HR Analytics System
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import os
from preprocessing import DataPreprocessor


class MLEngine:
    """Machine Learning engine for attrition and performance prediction"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.preprocessor = DataPreprocessor()
        self.attrition_model = None
        self.performance_model = None
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
    
    def create_attrition_target(self, df):
        """
        Create attrition target based on employee features
        This is a synthetic target for demonstration purposes
        
        Args:
            df: DataFrame with employee data
            
        Returns:
            Series with attrition labels (0: Stay, 1: Leave)
        """
        # Complex logic to simulate attrition likelihood
        attrition = []
        
        for _, row in df.iterrows():
            score = 0
            
            # Low satisfaction increases attrition
            if row['job_satisfaction'] <= 2:
                score += 3
            elif row['job_satisfaction'] == 3:
                score += 1
            
            # Poor work-life balance increases attrition
            if row['work_life_balance'] <= 2:
                score += 2
            
            # Overtime increases attrition
            if row['overtime'] == 'Yes':
                score += 2
            
            # Low performance might lead to leaving
            if row['performance_rating'] == 1:
                score += 2
            
            # Long tenure without promotion
            if row['years_at_company'] > 5 and row['promotion_history'] == 0:
                score += 2
            
            # Young employees in certain conditions
            if row['age'] < 30 and row['years_at_company'] < 2:
                score += 1
            
            # Random factor for variability
            score += np.random.randint(-2, 3)
            
            # Threshold for attrition
            attrition.append(1 if score >= 4 else 0)
        
        return pd.Series(attrition)
    
    def train_attrition_model(self, df):
        """
        Train Random Forest model for attrition prediction
        
        Args:
            df: DataFrame with employee data
            
        Returns:
            dict with model metrics
        """
        # Create synthetic attrition target
        df_with_target = df.copy()
        df_with_target['attrition'] = self.create_attrition_target(df)
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.preprocessor.prepare_data(
            df_with_target, target_column='attrition', fit=True
        )
        
        # Train Random Forest model
        self.attrition_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.attrition_model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.attrition_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Save model
        model_path = os.path.join(self.model_dir, 'attrition_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.attrition_model, f)
        
        # Save preprocessor
        preprocessor_path = os.path.join(self.model_dir, 'preprocessor.pkl')
        with open(preprocessor_path, 'wb') as f:
            pickle.dump(self.preprocessor, f)
        
        return {
            'accuracy': accuracy,
            'confusion_matrix': conf_matrix.tolist(),
            'samples_trained': len(X_train),
            'samples_tested': len(X_test)
        }
    
    def train_performance_model(self, df):
        """
        Train Random Forest model for performance prediction
        
        Args:
            df: DataFrame with employee data
            
        Returns:
            dict with model metrics
        """
        # Use performance_rating as target (1: Low, 2: Medium, 3: High)
        # Map to categorical labels
        performance_map = {1: 'Low', 2: 'Medium', 3: 'High'}
        df_with_target = df.copy()
        df_with_target['performance_category'] = df['performance_rating']
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.preprocessor.prepare_data(
            df_with_target.drop(columns=['performance_rating']), 
            target_column='performance_category', 
            fit=True
        )
        
        # Train Random Forest model
        self.performance_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.performance_model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.performance_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Save model
        model_path = os.path.join(self.model_dir, 'performance_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.performance_model, f)
        
        return {
            'accuracy': accuracy,
            'confusion_matrix': conf_matrix.tolist(),
            'samples_trained': len(X_train),
            'samples_tested': len(X_test)
        }
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            # Load attrition model
            attrition_path = os.path.join(self.model_dir, 'attrition_model.pkl')
            if os.path.exists(attrition_path):
                with open(attrition_path, 'rb') as f:
                    self.attrition_model = pickle.load(f)
            
            # Load performance model
            performance_path = os.path.join(self.model_dir, 'performance_model.pkl')
            if os.path.exists(performance_path):
                with open(performance_path, 'rb') as f:
                    self.performance_model = pickle.load(f)
            
            # Load preprocessor
            preprocessor_path = os.path.join(self.model_dir, 'preprocessor.pkl')
            if os.path.exists(preprocessor_path):
                with open(preprocessor_path, 'rb') as f:
                    self.preprocessor = pickle.load(f)
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict_attrition(self, employee_data):
        """
        Predict attrition risk for an employee
        
        Args:
            employee_data: dict with employee features
            
        Returns:
            dict with prediction and confidence
        """
        if self.attrition_model is None:
            raise ValueError("Attrition model not trained or loaded")
        
        # Prepare data
        X = self.preprocessor.prepare_single_prediction(employee_data)
        
        # Make prediction
        prediction = self.attrition_model.predict(X)[0]
        probabilities = self.attrition_model.predict_proba(X)[0]
        
        # Get confidence (probability of predicted class)
        confidence = probabilities[prediction] * 100
        
        result = "Leave" if prediction == 1 else "Stay"
        
        return {
            'result': result,
            'confidence': round(confidence, 2),
            'risk_score': round(probabilities[1] * 100, 2)  # Probability of leaving
        }
    
    def predict_performance(self, employee_data):
        """
        Predict performance level for an employee
        
        Args:
            employee_data: dict with employee features
            
        Returns:
            dict with prediction and confidence
        """
        if self.performance_model is None:
            raise ValueError("Performance model not trained or loaded")
        
        # Prepare data (exclude performance_rating from features)
        employee_data_copy = employee_data.copy()
        if 'performance_rating' in employee_data_copy:
            del employee_data_copy['performance_rating']
        
        X = self.preprocessor.prepare_single_prediction(employee_data_copy)
        
        # Make prediction
        prediction = self.performance_model.predict(X)[0]
        probabilities = self.performance_model.predict_proba(X)[0]
        
        # Map prediction to label
        performance_map = {1: 'Low', 2: 'Medium', 3: 'High'}
        result = performance_map.get(prediction, 'Medium')
        
        # Get confidence
        confidence = probabilities[prediction - 1] * 100
        
        return {
            'result': result,
            'confidence': round(confidence, 2),
            'level': int(prediction)
        }
