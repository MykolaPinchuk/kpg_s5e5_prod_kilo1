"""
Complete model pipeline for calorie expenditure prediction.
Handles data loading, preprocessing, feature engineering, training, and inference.
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_log_error, mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import multiprocessing

from .data_preprocessing import preprocess_data, validate_data
from .feature_engineering import create_essential_features, create_advanced_features, get_feature_columns


def calculate_rmsle(y_true, y_pred):
    """Calculate Root Mean Squared Logarithmic Error."""
    y_true = np.maximum(y_true, 1e-8)
    y_pred = np.maximum(y_pred, 1e-8)
    return np.sqrt(mean_squared_log_error(y_true, y_pred))


def create_baseline_xgb_model():
    """
    Create the baseline XGBoost model with optimized hyperparameters.
    Fast training (<3 seconds) with good performance (~0.07 RMSLE).
    """
    n_jobs = multiprocessing.cpu_count()
    
    baseline_xgb = xgb.XGBRegressor(
        objective='reg:squarederror',
        eval_metric='rmse',
        random_state=42,
        n_jobs=n_jobs,
        tree_method='hist',  # Fast histogram-based method
        verbosity=0,
        # Small and fast configuration
        n_estimators=100,
        max_depth=4,
        learning_rate=0.2,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        reg_alpha=0,
        reg_lambda=1
    )
    
    return baseline_xgb


def create_advanced_xgb_model():
    """
    Create an advanced XGBoost model for better performance.
    Slower training but improved accuracy.
    """
    n_jobs = multiprocessing.cpu_count()
    
    advanced_xgb = xgb.XGBRegressor(
        objective='reg:squarederror',
        eval_metric='rmse',
        random_state=42,
        n_jobs=n_jobs,
        tree_method='hist',
        verbosity=0,
        # More sophisticated configuration
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=2,
        reg_alpha=0.1,
        reg_lambda=1.2
    )
    
    return advanced_xgb


def train_model(train_data_path, model_type='baseline', feature_type='essential', 
                test_size=0.2, validation_size=0.2, random_state=42):
    """
    Complete training pipeline from raw data to trained model.
    
    Args:
        train_data_path (str): Path to training CSV file
        model_type (str): 'baseline' or 'advanced'
        feature_type (str): 'essential' or 'advanced'
        test_size (float): Proportion for test split
        validation_size (float): Proportion for validation split (from remaining data)
        random_state (int): Random seed for reproducibility
    
    Returns:
        dict: Training results including model, metrics, and feature info
    """
    # Load and validate data
    train_df = pd.read_csv(train_data_path)
    validation_results = validate_data(train_df, is_training_data=True)
    
    if not validation_results['valid']:
        raise ValueError(f"Data validation failed: {validation_results['errors']}")
    
    # Preprocess data
    train_processed = preprocess_data(train_df)
    
    # Create features
    if feature_type == 'essential':
        train_features, new_features = create_essential_features(train_processed)
    elif feature_type == 'advanced':
        train_features, essential_features = create_essential_features(train_processed)
        train_features, advanced_features = create_advanced_features(train_features)
        new_features = essential_features + advanced_features
    else:
        raise ValueError("feature_type must be 'essential' or 'advanced'")
    
    # Prepare features and target
    feature_columns = get_feature_columns(train_features, include_target=False)
    X = train_features[feature_columns]
    y = train_features['Calories']
    
    # Split data: train/temp, then temp -> validation/test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=(test_size + validation_size), random_state=random_state
    )
    
    # Split temp into validation and test
    val_test_ratio = test_size / (test_size + validation_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=val_test_ratio, random_state=random_state
    )
    
    # Create and train model
    if model_type == 'baseline':
        model = create_baseline_xgb_model()
    elif model_type == 'advanced':
        model = create_advanced_xgb_model()
    else:
        raise ValueError("model_type must be 'baseline' or 'advanced'")
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'train_rmse': float(np.sqrt(mean_squared_error(y_train, y_train_pred))),
        'train_rmsle': float(calculate_rmsle(y_train, y_train_pred)),
        'train_r2': float(r2_score(y_train, y_train_pred)),
        'train_mae': float(mean_absolute_error(y_train, y_train_pred)),
        
        'val_rmse': float(np.sqrt(mean_squared_error(y_val, y_val_pred))),
        'val_rmsle': float(calculate_rmsle(y_val, y_val_pred)),
        'val_r2': float(r2_score(y_val, y_val_pred)),
        'val_mae': float(mean_absolute_error(y_val, y_val_pred)),
        
        'test_rmse': float(np.sqrt(mean_squared_error(y_test, y_test_pred))),
        'test_rmsle': float(calculate_rmsle(y_test, y_test_pred)),
        'test_r2': float(r2_score(y_test, y_test_pred)),
        'test_mae': float(mean_absolute_error(y_test, y_test_pred)),
    }
    
    # Calculate overfitting ratio
    metrics['overfitting_ratio'] = metrics['val_rmsle'] / metrics['train_rmsle'] if metrics['train_rmsle'] > 0 else 1.0
    
    return {
        'model': model,
        'metrics': metrics,
        'feature_columns': feature_columns,
        'new_features': new_features,
        'model_type': model_type,
        'feature_type': feature_type,
        'data_splits': {
            'train_size': len(X_train),
            'val_size': len(X_val), 
            'test_size': len(X_test)
        }
    }


def predict(model, test_data_path, feature_columns=None, feature_type='essential'):
    """
    Make predictions on new data using trained model.
    
    Args:
        model: Trained XGBoost model
        test_data_path (str): Path to test CSV file
        feature_columns (list): List of feature columns (if None, will be inferred)
        feature_type (str): 'essential' or 'advanced' - must match training
    
    Returns:
        dict: Predictions and metadata
    """
    # Load and validate test data
    test_df = pd.read_csv(test_data_path)
    validation_results = validate_data(test_df, is_training_data=False)
    
    if not validation_results['valid']:
        raise ValueError(f"Test data validation failed: {validation_results['errors']}")
    
    # Preprocess data
    test_processed = preprocess_data(test_df)
    
    # Create features (same as training)
    if feature_type == 'essential':
        test_features, _ = create_essential_features(test_processed)
    elif feature_type == 'advanced':
        test_features, _ = create_essential_features(test_processed)
        test_features, _ = create_advanced_features(test_features)
    else:
        raise ValueError("feature_type must be 'essential' or 'advanced'")
    
    # Get feature columns
    if feature_columns is None:
        feature_columns = get_feature_columns(test_features, include_target=False)
    
    # Ensure all required features are present
    missing_features = [col for col in feature_columns if col not in test_features.columns]
    if missing_features:
        raise ValueError(f"Missing required features in test data: {missing_features}")
    
    # Make predictions
    X_test = test_features[feature_columns]
    predictions = model.predict(X_test)
    
    return {
        'predictions': predictions,
        'test_ids': test_df['id'].values,
        'feature_columns_used': feature_columns,
        'num_samples': len(predictions),
        'prediction_range': {
            'min': float(predictions.min()),
            'max': float(predictions.max()),
            'mean': float(predictions.mean())
        }
    }


def save_model(model, filepath, metadata=None):
    """Save trained model with metadata."""
    model_data = {
        'model': model,
        'metadata': metadata or {}
    }
    joblib.dump(model_data, filepath)


def load_model(filepath):
    """Load trained model and metadata."""
    model_data = joblib.load(filepath)
    if isinstance(model_data, dict) and 'model' in model_data:
        return model_data['model'], model_data.get('metadata', {})
    else:
        # Handle legacy format (just the model)
        return model_data, {}


def create_submission(model, test_data_path, submission_path, feature_columns=None, feature_type='essential'):
    """
    Create a submission file for Kaggle competition.
    
    Args:
        model: Trained XGBoost model
        test_data_path (str): Path to test CSV file
        submission_path (str): Path to save submission CSV
        feature_columns (list): Feature columns used in training
        feature_type (str): Feature type used in training
    
    Returns:
        pd.DataFrame: Submission dataframe
    """
    # Make predictions
    prediction_results = predict(model, test_data_path, feature_columns, feature_type)
    
    # Create submission format
    submission_df = pd.DataFrame({
        'id': prediction_results['test_ids'],
        'Calories': prediction_results['predictions']
    })
    
    # Save submission
    submission_df.to_csv(submission_path, index=False)
    
    return submission_df