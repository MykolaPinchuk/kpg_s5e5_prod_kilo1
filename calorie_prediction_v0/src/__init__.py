"""
Calorie expenditure prediction model pipeline.
"""
from .data_preprocessing import preprocess_data, validate_data
from .feature_engineering import create_essential_features, create_advanced_features, get_feature_columns
from .model_pipeline import (
    train_model, predict, create_baseline_xgb_model, create_advanced_xgb_model,
    save_model, load_model, create_submission, calculate_rmsle
)

__version__ = "1.0.0"