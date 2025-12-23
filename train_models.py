"""
School Recommendation System - Model Training Script
Uses the actual Phoenix Schools dataset from GitHub repository
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
import joblib
import os

def train_models():
    """Train models on the actual school dataset"""
    print("Loading dataset...")
    
    # Load the actual dataset
    school_raw_data = pd.read_csv("511_project_Step_3.csv")
    
    print(f"Dataset shape: {school_raw_data.shape}")
    print(f"Number of schools: {len(school_raw_data)}")
    print(f"Columns: {school_raw_data.columns.tolist()[:10]}...")
    
    # Make a copy for processing
    school_data = school_raw_data.copy(deep=True)
    
    # Encode categorical variables
    print("\nEncoding categorical variables...")
    city_encoder = LabelEncoder()
    school_data['city'] = city_encoder.fit_transform(school_raw_data['city'])
    
    zipcode_encoder = LabelEncoder()
    school_data['zipcode'] = zipcode_encoder.fit_transform(school_raw_data['zipcode'])
    
    # Drop expense columns (columns 33-37 as per original code)
    expense_columns = school_raw_data.columns[33:37].tolist()
    print(f"Dropping expense columns: {expense_columns}")
    school_data.drop(columns=expense_columns, inplace=True, axis=1)
    
    # Prepare output data (keep school names)
    school_output_data = school_data.copy(deep=True)
    
    # Standardize features (exclude School_name column)
    print("\nStandardizing features...")
    scaler = StandardScaler()
    school_data_scaled = pd.DataFrame(
        scaler.fit_transform(school_data.iloc[:, 1:]),  # Skip School_name column
        columns=school_data.columns[1:]
    )
    
    # Train models
    print("\nTraining K-Nearest Neighbors model...")
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(school_data_scaled, school_output_data['School_name'])
    print("✓ KNN model trained")
    
    print("\nTraining Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=5, random_state=42, max_depth=15)
    rf_model.fit(school_data_scaled, school_output_data['School_name'])
    print("✓ Random Forest model trained")
    
    print("\nTraining Support Vector Machine model...")
    svm_model = SVC(probability=True, random_state=42, kernel='rbf')
    svm_model.fit(school_data_scaled, school_output_data['School_name'])
    print("✓ SVM model trained")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save everything
    print("\nSaving models and data...")
    joblib.dump(knn_model, 'models/knn_model.pkl')
    joblib.dump(rf_model, 'models/rf_model.pkl')
    joblib.dump(svm_model, 'models/svm_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(city_encoder, 'models/city_encoder.pkl')
    joblib.dump(zipcode_encoder, 'models/zipcode_encoder.pkl')
    joblib.dump(school_raw_data, 'models/school_raw_data.pkl')
    joblib.dump(school_data_scaled, 'models/school_data_scaled.pkl')
    joblib.dump(school_data.columns[1:].tolist(), 'models/feature_columns.pkl')
    
    print("\n" + "=" * 60)
    print("✓ Training complete!")
    print(f"✓ {len(school_raw_data)} schools processed")
    print(f"✓ {len(school_data_scaled.columns)} features")
    print(f"✓ Models saved in 'models/' directory")
    print("=" * 60)
    
    return knn_model, rf_model, svm_model

if __name__ == "__main__":
    print("=" * 60)
    print("School Recommendation System - Model Training")
    print("=" * 60)
    print()
    
    train_models()
