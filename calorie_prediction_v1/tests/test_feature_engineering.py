"""
Basic tests for feature engineering pipeline.
"""
import unittest
import os
import sys

# Add the virtual environment's site-packages to the path
venv_site_packages = os.path.join(os.path.dirname(__file__), '..', 'venv', 'lib', 'python3.12', 'site-packages')
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

import pandas as pd
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.data_preprocessing import preprocess_data
from src.feature_engineering import create_essential_features, create_advanced_features, get_feature_columns


class TestFeatureEngineering(unittest.TestCase):
    """Test cases for feature engineering functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_subsample.csv')
        
        # Load and preprocess sample data
        test_df = pd.read_csv(self.test_data_path)
        self.processed_df = preprocess_data(test_df)
    
    def test_create_essential_features_function_exists(self):
        """Test that the create_essential_features function exists."""
        self.assertTrue(callable(create_essential_features), "create_essential_features function should be callable")
    
    def test_create_essential_features(self):
        """Test creation of essential features."""
        try:
            df_with_features, new_features = create_essential_features(self.processed_df)
            
            # Check that result is a DataFrame
            self.assertIsInstance(df_with_features, pd.DataFrame, "Result should be a DataFrame")
            
            # Check that new_features is a list
            self.assertIsInstance(new_features, list, "New features should be a list")
            
            # Check that essential features are created
            essential_features = [
                'BMI',
                'Duration_HR_interaction',
                'Weight_HR_interaction',
                'MET_estimated',
                'MET_Duration_product',
                'Temp_deviation',
                'Duration_HR_Temp_interaction'
            ]
            
            for feature in essential_features:
                self.assertIn(feature, df_with_features.columns, f"Feature {feature} should exist")
            
            # Check that new_features list contains the expected features
            for feature in essential_features:
                self.assertIn(feature, new_features, f"Feature {feature} should be in new_features list")
            
            # Check that feature values are reasonable
            self.assertTrue((df_with_features['BMI'] > 0).all(), "BMI should be positive")
            self.assertTrue((df_with_features['Duration_HR_interaction'] >= 0).all(), "Duration_HR_interaction should be non-negative")
            
        except Exception as e:
            self.fail(f"Creating essential features failed with exception: {e}")
    
    def test_create_advanced_features_function_exists(self):
        """Test that the create_advanced_features function exists."""
        self.assertTrue(callable(create_advanced_features), "create_advanced_features function should be callable")
    
    def test_create_advanced_features(self):
        """Test creation of advanced features."""
        try:
            # First create essential features
            df_with_essential, _ = create_essential_features(self.processed_df)
            
            # Then create advanced features
            df_with_advanced, new_features = create_advanced_features(df_with_essential)
            
            # Check that result is a DataFrame
            self.assertIsInstance(df_with_advanced, pd.DataFrame, "Result should be a DataFrame")
            
            # Check that new_features is a list
            self.assertIsInstance(new_features, list, "New features should be a list")
            
            # Check that some advanced features are created
            advanced_features = [
                'BMI_category_underweight',
                'BMI_category_normal',
                'BMI_category_overweight',
                'BMI_category_obese',
                'Age_group_young',
                'Age_group_middle',
                'Age_group_senior'
            ]
            
            for feature in advanced_features:
                self.assertIn(feature, df_with_advanced.columns, f"Feature {feature} should exist")
            
            # Check that BMI categories are mutually exclusive and collectively exhaustive
            bmi_category_cols = ['BMI_category_underweight', 'BMI_category_normal', 'BMI_category_overweight', 'BMI_category_obese']
            bmi_category_sum = df_with_advanced[bmi_category_cols].sum(axis=1)
            self.assertTrue((bmi_category_sum == 1).all(), "Each row should belong to exactly one BMI category")
            
        except Exception as e:
            self.fail(f"Creating advanced features failed with exception: {e}")
    
    def test_get_feature_columns_function_exists(self):
        """Test that the get_feature_columns function exists."""
        self.assertTrue(callable(get_feature_columns), "get_feature_columns function should be callable")
    
    def test_get_feature_columns(self):
        """Test getting feature columns."""
        try:
            # Create features
            df_with_features, _ = create_essential_features(self.processed_df)
            
            # Get feature columns without target
            feature_cols = get_feature_columns(df_with_features, include_target=False)
            
            # Check that result is a list
            self.assertIsInstance(feature_cols, list, "Feature columns should be a list")
            
            # Check that id column is not included
            self.assertNotIn('id', feature_cols, "id column should not be included")
            
            # Check that Calories column is not included when include_target=False
            self.assertNotIn('Calories', feature_cols, "Calories column should not be included when include_target=False")
            
            # Get feature columns with target
            feature_cols_with_target = get_feature_columns(df_with_features, include_target=True)
            
            # Check that Calories column is included when include_target=True
            # (Note: test data doesn't have Calories column, so this might not be present)
            
        except Exception as e:
            self.fail(f"Getting feature columns failed with exception: {e}")


if __name__ == '__main__':
    unittest.main()