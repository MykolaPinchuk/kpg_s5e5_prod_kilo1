"""
Basic tests for data preprocessing pipeline.
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

from src.data_preprocessing import preprocess_data, validate_data


class TestDataPreprocessing(unittest.TestCase):
    """Test cases for data preprocessing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_subsample.csv')
        self.train_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'train_subsample.csv')
        
        # Load sample data
        self.test_df = pd.read_csv(self.test_data_path)
        self.train_df = pd.read_csv(self.train_data_path)
    
    def test_preprocess_data_function_exists(self):
        """Test that the preprocess_data function exists."""
        self.assertTrue(callable(preprocess_data), "preprocess_data function should be callable")
    
    def test_preprocess_test_data(self):
        """Test preprocessing of test data."""
        try:
            processed_df = preprocess_data(self.test_df)
            
            # Check that result is a DataFrame
            self.assertIsInstance(processed_df, pd.DataFrame, "Result should be a DataFrame")
            
            # Check that required columns exist
            required_cols = ['id', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
            for col in required_cols:
                self.assertIn(col, processed_df.columns, f"Column {col} should exist")
            
            # Check that gender columns are created
            self.assertIn('Sex_female', processed_df.columns, "Sex_female column should exist")
            self.assertIn('Sex_male', processed_df.columns, "Sex_male column should exist")
            
            # Check that gender columns have correct values (0 or 1)
            self.assertTrue(processed_df['Sex_female'].isin([0, 1]).all(), "Sex_female should contain only 0 or 1")
            self.assertTrue(processed_df['Sex_male'].isin([0, 1]).all(), "Sex_male should contain only 0 or 1")
            
        except Exception as e:
            self.fail(f"Preprocessing test data failed with exception: {e}")
    
    def test_preprocess_train_data(self):
        """Test preprocessing of training data."""
        try:
            processed_df = preprocess_data(self.train_df)
            
            # Check that result is a DataFrame
            self.assertIsInstance(processed_df, pd.DataFrame, "Result should be a DataFrame")
            
            # Check that required columns exist
            required_cols = ['id', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp', 'Calories']
            for col in required_cols:
                self.assertIn(col, processed_df.columns, f"Column {col} should exist")
            
            # Check that gender columns are created
            self.assertIn('Sex_female', processed_df.columns, "Sex_female column should exist")
            self.assertIn('Sex_male', processed_df.columns, "Sex_male column should exist")
            
        except Exception as e:
            self.fail(f"Preprocessing train data failed with exception: {e}")
    
    def test_validate_data_function_exists(self):
        """Test that the validate_data function exists."""
        self.assertTrue(callable(validate_data), "validate_data function should be callable")
    
    def test_validate_test_data(self):
        """Test validation of test data."""
        try:
            validation_results = validate_data(self.test_df, is_training_data=False)
            
            # Check that result is a dictionary
            self.assertIsInstance(validation_results, dict, "Validation results should be a dictionary")
            
            # Check that required keys exist
            self.assertIn('valid', validation_results, "Validation results should contain 'valid' key")
            self.assertIn('warnings', validation_results, "Validation results should contain 'warnings' key")
            self.assertIn('errors', validation_results, "Validation results should contain 'errors' key")
            
        except Exception as e:
            self.fail(f"Validating test data failed with exception: {e}")
    
    def test_validate_train_data(self):
        """Test validation of training data."""
        try:
            validation_results = validate_data(self.train_df, is_training_data=True)
            
            # Check that result is a dictionary
            self.assertIsInstance(validation_results, dict, "Validation results should be a dictionary")
            
            # Check that required keys exist
            self.assertIn('valid', validation_results, "Validation results should contain 'valid' key")
            self.assertIn('warnings', validation_results, "Validation results should contain 'warnings' key")
            self.assertIn('errors', validation_results, "Validation results should contain 'errors' key")
            
        except Exception as e:
            self.fail(f"Validating train data failed with exception: {e}")


if __name__ == '__main__':
    unittest.main()