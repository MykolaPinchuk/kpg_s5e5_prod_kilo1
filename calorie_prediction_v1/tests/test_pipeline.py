"""
Test suite for the calorie prediction pipeline.
"""
import unittest
import sys
import os

# Add the virtual environment's site-packages to the path
venv_site_packages = os.path.join(os.path.dirname(__file__), '..', 'venv', 'lib', 'python3.12', 'site-packages')
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model_pipeline import load_model, predict
from src.data_preprocessing import preprocess_data, validate_data
from src.feature_engineering import create_essential_features
import pandas as pd
import numpy as np

class TestCaloriePredictionPipeline(unittest.TestCase):
    """Test cases for the calorie prediction pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'baseline_xgb_model.pkl')
        cls.test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_subsample.csv')
        
        # Check if files exist
        if not os.path.exists(cls.model_path):
            raise FileNotFoundError(f"Model file not found at {cls.model_path}")
        
        if not os.path.exists(cls.test_data_path):
            raise FileNotFoundError(f"Test data file not found at {cls.test_data_path}")
    
    def test_model_loading(self):
        """Test that the model loads successfully."""
        model, metadata = load_model(self.model_path)
        self.assertIsNotNone(model)
        print(f"Model loaded successfully. Type: {type(model)}")
    
    def test_data_loading_and_validation(self):
        """Test that test data loads and validates successfully."""
        # Load test data
        test_df = pd.read_csv(self.test_data_path)
        self.assertIsNotNone(test_df)
        self.assertGreater(len(test_df), 0)
        
        # Validate data
        validation_results = validate_data(test_df, is_training_data=False)
        self.assertTrue(validation_results['valid'])
        
        print(f"Test data loaded successfully. Rows: {len(test_df)}")
        if validation_results['warnings']:
            print(f"Validation warnings: {validation_results['warnings']}")
    
    def test_preprocessing(self):
        """Test data preprocessing."""
        # Load test data
        test_df = pd.read_csv(self.test_data_path)
        
        # Preprocess data
        processed_df = preprocess_data(test_df)
        self.assertIsNotNone(processed_df)
        self.assertEqual(len(processed_df), len(test_df))
        
        # Check that required columns exist
        required_cols = ['id', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
        for col in required_cols:
            self.assertIn(col, processed_df.columns)
        
        print("Data preprocessing completed successfully")
    
    def test_feature_engineering(self):
        """Test feature engineering."""
        # Load and preprocess test data
        test_df = pd.read_csv(self.test_data_path)
        processed_df = preprocess_data(test_df)
        
        # Create features
        features_df, new_features = create_essential_features(processed_df)
        self.assertIsNotNone(features_df)
        self.assertEqual(len(features_df), len(processed_df))
        self.assertGreater(len(new_features), 0)
        
        # Check that new features were created
        expected_features = ['BMI', 'Duration_HR_interaction', 'Weight_HR_interaction',
                           'MET_estimated', 'MET_Duration_product', 'Temp_deviation',
                           'Duration_HR_Temp_interaction']
        
        for feature in expected_features:
            self.assertIn(feature, features_df.columns)
        
        print(f"Feature engineering completed. New features: {len(new_features)}")
    
    def test_prediction_pipeline(self):
        """Test the complete prediction pipeline."""
        # Load model
        model, metadata = load_model(self.model_path)
        self.assertIsNotNone(model)
        
        # Make predictions using the predict function
        prediction_results = predict(
            model=model,
            test_data_path=self.test_data_path,
            feature_type='essential'
        )
        
        # Check results
        self.assertIn('predictions', prediction_results)
        self.assertIn('test_ids', prediction_results)
        self.assertIn('num_samples', prediction_results)
        self.assertIn('prediction_range', prediction_results)
        
        predictions = prediction_results['predictions']
        self.assertIsNotNone(predictions)
        self.assertGreater(len(predictions), 0)
        
        # Check that predictions are reasonable
        self.assertTrue(np.all(predictions >= 0))  # Calories should be non-negative
        self.assertTrue(np.all(np.isfinite(predictions)))  # Should not contain NaN or Inf
        
        print(f"Prediction pipeline completed. Samples: {len(predictions)}")
        print(f"Prediction range: {prediction_results['prediction_range']}")


if __name__ == "__main__":
    unittest.main()