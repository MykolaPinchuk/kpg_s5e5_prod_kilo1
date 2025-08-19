"""
Basic tests for inference functionality.
"""
import unittest
import os
import sys
import pandas as pd
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model_pipeline import load_model, predict, create_submission
from data_preprocessing import preprocess_data, validate_data
from feature_engineering import create_essential_features


class TestInference(unittest.TestCase):
    """Test cases for inference functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'baseline_xgb_model.pkl')
        self.test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_subsample.csv')
        self.model, self.metadata = load_model(self.model_path)
    
    def test_predict_function_exists(self):
        """Test that the predict function exists."""
        self.assertTrue(callable(predict), "Predict function should be callable")
    
    def test_predict_with_test_data(self):
        """Test that predictions can be made on test data."""
        try:
            results = predict(
                model=self.model,
                test_data_path=self.test_data_path,
                feature_type='essential'
            )
            
            # Check that results are returned
            self.assertIsInstance(results, dict, "Results should be a dictionary")
            self.assertIn('predictions', results, "Results should contain predictions")
            self.assertIn('num_samples', results, "Results should contain num_samples")
            self.assertIn('prediction_range', results, "Results should contain prediction_range")
            
            # Check that we have predictions
            predictions = results['predictions']
            self.assertGreater(len(predictions), 0, "Should have at least one prediction")
            
            # Check prediction range
            prediction_range = results['prediction_range']
            self.assertGreaterEqual(prediction_range['min'], 0, "Predictions should be non-negative")
            self.assertGreater(prediction_range['max'], 0, "Predictions should be positive")
            
        except Exception as e:
            self.fail(f"Prediction failed with exception: {e}")
    
    def test_create_submission(self):
        """Test that submission files can be created."""
        try:
            submission_path = os.path.join(os.path.dirname(__file__), 'test_submission.csv')
            
            # Create submission
            submission_df = create_submission(
                model=self.model,
                test_data_path=self.test_data_path,
                submission_path=submission_path,
                feature_type='essential'
            )
            
            # Check that submission was created
            self.assertIsInstance(submission_df, pd.DataFrame, "Submission should be a DataFrame")
            self.assertGreater(len(submission_df), 0, "Submission should have rows")
            self.assertIn('id', submission_df.columns, "Submission should have id column")
            self.assertIn('Calories', submission_df.columns, "Submission should have Calories column")
            
            # Check that file was saved
            self.assertTrue(os.path.exists(submission_path), "Submission file should be created")
            
            # Clean up
            if os.path.exists(submission_path):
                os.remove(submission_path)
                
        except Exception as e:
            self.fail(f"Submission creation failed with exception: {e}")


if __name__ == '__main__':
    unittest.main()