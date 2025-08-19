"""
Test runner script to execute all tests.
"""
import unittest
import os
import sys

# Add the tests directory and the calorie_prediction_v0 directory to the path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import all test modules
from test_model_loading import TestModelLoading
from test_inference import TestInference
from test_data_preprocessing import TestDataPreprocessing
from test_feature_engineering import TestFeatureEngineering


def run_all_tests():
    """Run all tests and return the results."""
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests to the suite
    test_suite.addTest(unittest.makeSuite(TestModelLoading))
    test_suite.addTest(unittest.makeSuite(TestInference))
    test_suite.addTest(unittest.makeSuite(TestDataPreprocessing))
    test_suite.addTest(unittest.makeSuite(TestFeatureEngineering))
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(test_suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Running all tests...")
    success = run_all_tests()
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)