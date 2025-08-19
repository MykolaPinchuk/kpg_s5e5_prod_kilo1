"""
Data preprocessing pipeline for calorie expenditure prediction.
Handles missing values, categorical encoding, and data validation.
"""
import pandas as pd
import numpy as np


def preprocess_data(df):
    """
    Apply preprocessing transformations to raw data.
    
    Args:
        df (pd.DataFrame): Raw data with columns: id, Gender, Age, Height, Weight, 
                          Duration, Heart_Rate, Body_Temp, [Calories]
    
    Returns:
        pd.DataFrame: Preprocessed data ready for feature engineering
    """
    df_processed = df.copy()
    
    # Handle missing values (if any)
    numerical_columns = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
    for col in numerical_columns:
        if col in df_processed.columns and df_processed[col].isnull().any():
            df_processed[col].fillna(df_processed[col].mean(), inplace=True)
    
    # Handle categorical variables - One-hot encode Gender/Sex
    # Always ensure both Sex_female and Sex_male exist for deterministic feature schema
    if 'Gender' in df_processed.columns:
        dummies = pd.get_dummies(df_processed['Gender'], prefix='Sex')
        df_processed = df_processed.drop('Gender', axis=1)
    elif 'Sex' in df_processed.columns:
        dummies = pd.get_dummies(df_processed['Sex'], prefix='Sex')
        df_processed = df_processed.drop('Sex', axis=1)
    else:
        dummies = pd.DataFrame(index=df_processed.index)

    # Reindex to always include both columns in a fixed order
    dummies = dummies.reindex(columns=['Sex_female', 'Sex_male'], fill_value=0)
    for col in ['Sex_female', 'Sex_male']:
        if col not in df_processed.columns:
            df_processed[col] = dummies[col]
    
    # Ensure consistent column order
    feature_columns = [col for col in df_processed.columns if col not in ['id', 'Calories']]
    target_columns = ['Calories'] if 'Calories' in df_processed.columns else []
    df_processed = df_processed[['id'] + feature_columns + target_columns]
    
    return df_processed


def validate_data(df, is_training_data=True):
    """
    Validate that data has expected structure and ranges.
    
    Args:
        df (pd.DataFrame): Data to validate
        is_training_data (bool): Whether this is training data (has Calories column)
    
    Returns:
        dict: Validation results and warnings
    """
    validation_results = {'valid': True, 'warnings': [], 'errors': []}
    
    # Check required columns
    required_cols = ['id', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
    if is_training_data:
        required_cols.append('Calories')
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        validation_results['errors'].append(f"Missing required columns: {missing_cols}")
        validation_results['valid'] = False
    
    # Check for reasonable value ranges
    if 'Age' in df.columns:
        if df['Age'].min() < 10 or df['Age'].max() > 100:
            validation_results['warnings'].append("Age values outside expected range (10-100)")
    
    if 'Height' in df.columns:
        if df['Height'].min() < 100 or df['Height'].max() > 250:
            validation_results['warnings'].append("Height values outside expected range (100-250 cm)")
    
    if 'Weight' in df.columns:
        if df['Weight'].min() < 30 or df['Weight'].max() > 200:
            validation_results['warnings'].append("Weight values outside expected range (30-200 kg)")
    
    if 'Heart_Rate' in df.columns:
        if df['Heart_Rate'].min() < 50 or df['Heart_Rate'].max() > 220:
            validation_results['warnings'].append("Heart Rate values outside expected range (50-220 bpm)")
    
    if 'Body_Temp' in df.columns:
        if df['Body_Temp'].min() < 35 or df['Body_Temp'].max() > 42:
            validation_results['warnings'].append("Body Temperature outside expected range (35-42°C)")
    
    if is_training_data and 'Calories' in df.columns:
        if df['Calories'].min() < 0:
            validation_results['errors'].append("Negative calorie values found")
            validation_results['valid'] = False
    
    # Check for missing values
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        validation_results['warnings'].append(f"Missing values found: {missing_counts[missing_counts > 0].to_dict()}")
    
    return validation_results