"""
Feature engineering pipeline for calorie expenditure prediction.
Creates essential features for the XGBoost baseline model.
"""
import pandas as pd
import numpy as np


def create_essential_features(df):
    """
    Create essential engineered features for the baseline XGBoost model.
    
    Args:
        df (pd.DataFrame): Preprocessed data with basic features
    
    Returns:
        tuple: (df_with_features, list_of_new_feature_names)
    """
    df_features = df.copy()
    
    # Track original features to identify new ones
    original_features = [col for col in df.columns if col not in ['id', 'Calories']]
    
    # 1. BMI (fundamental body composition metric)
    df_features['BMI'] = df_features['Weight'] / ((df_features['Height'] / 100) ** 2)
    
    # 2. Core interaction features (top performers from feature importance analysis)
    df_features['Duration_HR_interaction'] = df_features['Duration'] * df_features['Heart_Rate']
    df_features['Weight_HR_interaction'] = df_features['Weight'] * df_features['Heart_Rate']
    
    # 3. Essential domain knowledge features
    # MET estimation (Metabolic Equivalent of Task) - simplified approach
    age_adjusted_max_hr = 220 - df_features['Age']
    hr_intensity = np.clip((df_features['Heart_Rate'] - 60) / (age_adjusted_max_hr - 60), 0, 1)
    df_features['MET_estimated'] = 1 + (hr_intensity * 10)  # Scale from 1-11 METs
    df_features['MET_Duration_product'] = df_features['MET_estimated'] * df_features['Duration']
    
    # 4. Temperature deviation (simple but effective physiological indicator)
    df_features['Temp_deviation'] = abs(df_features['Body_Temp'] - 37.0)
    
    # 5. Triple interaction (highest performing complex feature)
    df_features['Duration_HR_Temp_interaction'] = (df_features['Duration'] * 
                                                   df_features['Heart_Rate'] * 
                                                   df_features['Body_Temp'])
    
    # Identify new features
    all_features = [col for col in df_features.columns if col not in ['id', 'Calories']]
    new_features = [col for col in all_features if col not in original_features]
    
    return df_features, new_features


def create_advanced_features(df):
    """
    Create additional advanced features for improved model performance.
    Use this for more sophisticated models beyond the baseline.
    
    Args:
        df (pd.DataFrame): Data with essential features already created
    
    Returns:
        tuple: (df_with_advanced_features, list_of_new_feature_names)
    """
    df_advanced = df.copy()
    
    # Track features before adding advanced ones
    features_before = [col for col in df.columns if col not in ['id', 'Calories']]
    
    # BMI categories (clinical thresholds)
    df_advanced['BMI_category_underweight'] = (df_advanced['BMI'] < 18.5).astype(int)
    df_advanced['BMI_category_normal'] = ((df_advanced['BMI'] >= 18.5) & (df_advanced['BMI'] < 25)).astype(int)
    df_advanced['BMI_category_overweight'] = ((df_advanced['BMI'] >= 25) & (df_advanced['BMI'] < 30)).astype(int)
    df_advanced['BMI_category_obese'] = (df_advanced['BMI'] >= 30).astype(int)
    
    # Age-based features
    df_advanced['Age_group_young'] = (df_advanced['Age'] < 30).astype(int)
    df_advanced['Age_group_middle'] = ((df_advanced['Age'] >= 30) & (df_advanced['Age'] < 50)).astype(int)
    df_advanced['Age_group_senior'] = (df_advanced['Age'] >= 50).astype(int)
    df_advanced['Age_squared'] = df_advanced['Age'] ** 2
    
    # Duration-based workout categories
    df_advanced['Short_workout'] = (df_advanced['Duration'] < 30).astype(int)
    df_advanced['Medium_workout'] = ((df_advanced['Duration'] >= 30) & (df_advanced['Duration'] < 60)).astype(int)
    df_advanced['Long_workout'] = (df_advanced['Duration'] >= 60).astype(int)
    df_advanced['Duration_squared'] = df_advanced['Duration'] ** 2
    
    # Heart rate zones (exercise physiology based)
    df_advanced['HR_zone_low'] = (df_advanced['Heart_Rate'] < 120).astype(int)
    df_advanced['HR_zone_moderate'] = ((df_advanced['Heart_Rate'] >= 120) & (df_advanced['Heart_Rate'] < 150)).astype(int)
    df_advanced['HR_zone_vigorous'] = (df_advanced['Heart_Rate'] >= 150).astype(int)
    
    # Temperature indicators
    df_advanced['High_body_temp'] = (df_advanced['Body_Temp'] > 37.5).astype(int)
    df_advanced['Low_body_temp'] = (df_advanced['Body_Temp'] < 36.5).astype(int)
    
    # Gender-specific interactions (if gender columns exist)
    if 'Sex_male' in df_advanced.columns and 'Sex_female' in df_advanced.columns:
        df_advanced['Male_Weight_interaction'] = df_advanced['Sex_male'] * df_advanced['Weight']
        df_advanced['Female_Weight_interaction'] = df_advanced['Sex_female'] * df_advanced['Weight']
        df_advanced['Male_Age_interaction'] = df_advanced['Sex_male'] * df_advanced['Age']
        df_advanced['Female_Age_interaction'] = df_advanced['Sex_female'] * df_advanced['Age']
    
    # Additional interaction features
    df_advanced['Weight_Duration_interaction'] = df_advanced['Weight'] * df_advanced['Duration']
    df_advanced['Age_Duration_interaction'] = df_advanced['Age'] * df_advanced['Duration']
    df_advanced['BMI_Duration_interaction'] = df_advanced['BMI'] * df_advanced['Duration']
    
    # Efficiency metrics
    df_advanced['Duration_per_HR'] = df_advanced['Duration'] / df_advanced['Heart_Rate']
    
    # Identify new advanced features
    features_after = [col for col in df_advanced.columns if col not in ['id', 'Calories']]
    new_advanced_features = [col for col in features_after if col not in features_before]
    
    return df_advanced, new_advanced_features


def get_feature_columns(df, include_target=False):
    """
    Get list of feature columns (excluding id and optionally target).
    
    Args:
        df (pd.DataFrame): DataFrame with features
        include_target (bool): Whether to include Calories column if present
    
    Returns:
        list: List of feature column names
    """
    exclude_cols = ['id']
    if not include_target:
        exclude_cols.append('Calories')
    
    return [col for col in df.columns if col not in exclude_cols]