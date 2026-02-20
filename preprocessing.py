"""
Data preprocessing module for HR Analytics System
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    """Handles all data preprocessing tasks"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.categorical_features = ['gender', 'department', 'job_role', 'overtime']
        self.numerical_features = ['age', 'salary', 'years_at_company', 
                                  'job_satisfaction', 'work_life_balance', 
                                  'performance_rating', 'promotion_history']
    
    def handle_missing_values(self, df):
        """
        Handle missing values in the dataset
        
        Args:
            df: pandas DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        # For numerical columns, fill with median
        for col in self.numerical_features:
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        for col in self.categorical_features:
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        return df
    
    def encode_categorical_features(self, df, fit=True):
        """
        Encode categorical features using LabelEncoder
        
        Args:
            df: pandas DataFrame
            fit: whether to fit the encoder (True for training, False for prediction)
            
        Returns:
            DataFrame with encoded categorical features
        """
        df_encoded = df.copy()
        
        for feature in self.categorical_features:
            if feature in df_encoded.columns:
                if fit:
                    # Fit and transform for training data
                    self.label_encoders[feature] = LabelEncoder()
                    df_encoded[feature] = self.label_encoders[feature].fit_transform(
                        df_encoded[feature].astype(str)
                    )
                else:
                    # Transform only for prediction data
                    if feature in self.label_encoders:
                        # Handle unseen categories
                        le = self.label_encoders[feature]
                        df_encoded[feature] = df_encoded[feature].astype(str).apply(
                            lambda x: le.transform([x])[0] if x in le.classes_ else -1
                        )
        
        return df_encoded
    
    def normalize_features(self, df, fit=True):
        """
        Normalize numerical features using StandardScaler
        
        Args:
            df: pandas DataFrame
            fit: whether to fit the scaler (True for training, False for prediction)
            
        Returns:
            DataFrame with normalized numerical features
        """
        df_normalized = df.copy()
        
        # Get numerical features that exist in the dataframe
        features_to_scale = [f for f in self.numerical_features if f in df_normalized.columns]
        
        if features_to_scale:
            if fit:
                df_normalized[features_to_scale] = self.scaler.fit_transform(
                    df_normalized[features_to_scale]
                )
            else:
                df_normalized[features_to_scale] = self.scaler.transform(
                    df_normalized[features_to_scale]
                )
        
        return df_normalized
    
    def prepare_data(self, df, target_column=None, fit=True, test_size=0.2, random_state=42):
        """
        Complete data preparation pipeline
        
        Args:
            df: pandas DataFrame
            target_column: name of target column (None for prediction mode)
            fit: whether to fit preprocessors
            test_size: proportion of test set
            random_state: random seed
            
        Returns:
            If target_column is provided: X_train, X_test, y_train, y_test
            If target_column is None: X_processed
        """
        # Handle missing values
        df_clean = self.handle_missing_values(df)
        
        # Separate features and target
        if target_column and target_column in df_clean.columns:
            X = df_clean.drop(columns=[target_column])
            y = df_clean[target_column]
        else:
            X = df_clean.copy()
            y = None
        
        # Encode categorical features
        X_encoded = self.encode_categorical_features(X, fit=fit)
        
        # Normalize numerical features
        X_processed = self.normalize_features(X_encoded, fit=fit)
        
        # Split data if target is provided
        if y is not None:
            X_train, X_test, y_train, y_test = train_test_split(
                X_processed, y, test_size=test_size, random_state=random_state
            )
            return X_train, X_test, y_train, y_test
        else:
            return X_processed
    
    def prepare_single_prediction(self, employee_data):
        """
        Prepare a single employee record for prediction
        
        Args:
            employee_data: dict with employee features
            
        Returns:
            Processed feature array ready for prediction
        """
        # Convert to DataFrame
        df = pd.DataFrame([employee_data])
        
        # Preprocess (fit=False to use existing encoders/scalers)
        X_processed = self.prepare_data(df, fit=False)
        
        return X_processed
    
    def get_feature_names(self):
        """Get list of feature names in order"""
        return self.numerical_features + self.categorical_features
