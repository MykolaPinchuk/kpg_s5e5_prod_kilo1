"""
Basic tests for model loading functionality.
"""
import unittest
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model_pipeline import load_model


class TestModelLoading(unittest.TestCase):
    """Test cases for model loading functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'baseline_xgb_model.pkl')
    
    def test_model_file_exists(self):
        """Test that the model file exists."""
        self.assertTrue(os.path.exists(self.model_path), "Model file should exist")
    
    def test_load_model_success(self):
        """Test that the model can be loaded successfully."""
        try:
            model, metadata = load_model(self.model_path)
            self.assertIsNotNone(model, "Model should be loaded successfully")
            # Check that it's an XGBoost model
            self.assertTrue(hasattr(model, 'predict'), "Model should have predict method")
        except Exception as e:
            self.fail(f"Model loading failed with exception: {e}")
    
    def test_model_metadata(self):
        """Test that model metadata is loaded correctly."""
        model, metadata = load_model(self.model_path)
        # Metadata might be empty for this model, but shouldn't cause errors
        self.assertIsInstance(metadata, dict, "Metadata should be a dictionary")


if __name__ == '__main__':
    unittest.main()