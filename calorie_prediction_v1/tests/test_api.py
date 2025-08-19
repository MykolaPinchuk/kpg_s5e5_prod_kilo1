"""
Test suite for the calorie prediction API.
"""
import unittest
import time
import os
import subprocess
import sys

# Add the virtual environment's site-packages to the path
venv_site_packages = os.path.join(os.path.dirname(__file__), '..', 'venv', 'lib', 'python3.12', 'site-packages')
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

# Add the tests directory to the path so we can import test utilities
sys.path.insert(0, os.path.dirname(__file__))

try:
    from test_utils import is_docker_available
except ImportError:
    # Fallback if test_utils is not available
    def is_docker_available():
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False

import requests

class TestCaloriePredictionAPI(unittest.TestCase):
    """Test cases for the calorie prediction API."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        # Check if Docker is available
        if not is_docker_available():
            raise unittest.SkipTest("Docker is not available, skipping API tests")
        
        cls.base_url = "http://localhost:8000"
        cls.api_prefix = "/api/v1"
        
        # Start the Docker container
        try:
            # Build the Docker image
            build_result = subprocess.run(
                ["docker", "build", "-t", "calorie-prediction-api", "."],
                cwd="calorie_prediction_v1",
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if build_result.returncode != 0:
                raise Exception(f"Docker build failed: {build_result.stderr}")
            
            # Start the Docker container
            cls.container_process = subprocess.Popen([
                "docker", "run", "--rm", "-p", "8000:8000",
                "calorie-prediction-api"
            ], cwd="calorie_prediction_v1")
            
            # Wait for the service to start
            time.sleep(10)
            
        except Exception as e:
            cls.tearDownClass()
            raise Exception(f"Failed to start Docker container: {str(e)}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        # Stop the Docker container
        try:
            subprocess.run(["docker", "stop", "$(docker ps -q --filter ancestor=calorie-prediction-api)"],
                          capture_output=True, text=True, timeout=30)
        except:
            pass
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = requests.get(f"{self.base_url}{self.api_prefix}/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("version", data)
        self.assertEqual(data["status"], "healthy")
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
        self.assertIn("docs", data)
        self.assertIn("health", data)
    
    def test_prediction_endpoint_valid_data(self):
        """Test the prediction endpoint with valid data."""
        test_data = {
            "workouts": [
                {
                    "id": "test1",
                    "Gender": "male",
                    "Age": 30,
                    "Height": 175.0,
                    "Weight": 70.0,
                    "Duration": 30.0,
                    "Heart_Rate": 100.0,
                    "Body_Temp": 37.5
                },
                {
                    "id": "test2",
                    "Gender": "female",
                    "Age": 25,
                    "Height": 165.0,
                    "Weight": 60.0,
                    "Duration": 45.0,
                    "Heart_Rate": 120.0,
                    "Body_Temp": 38.0
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/predict",
            json=test_data
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("predictions", data)
        self.assertIn("workout_ids", data)
        self.assertIn("prediction_metadata", data)
        
        # Check that we have predictions for each workout
        self.assertEqual(len(data["predictions"]), len(test_data["workouts"]))
        self.assertEqual(len(data["workout_ids"]), len(test_data["workouts"]))
        
        # Check that predictions are reasonable numbers
        for prediction in data["predictions"]:
            self.assertIsInstance(prediction, (int, float))
            self.assertGreaterEqual(prediction, 0)  # Calories should be non-negative
    
    def test_prediction_endpoint_invalid_data(self):
        """Test the prediction endpoint with invalid data."""
        # Missing required fields
        invalid_data = {
            "workouts": [
                {
                    "id": "test1"
                    # Missing all other required fields
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/predict",
            json=invalid_data
        )
        
        # This should return a validation error (422)
        self.assertEqual(response.status_code, 422)
    
    def test_prediction_endpoint_out_of_range_values(self):
        """Test the prediction endpoint with out-of-range values."""
        # Values outside expected ranges
        out_of_range_data = {
            "workouts": [
                {
                    "id": "test1",
                    "Gender": "male",
                    "Age": 150,  # Too high
                    "Height": 175.0,
                    "Weight": 70.0,
                    "Duration": 30.0,
                    "Heart_Rate": 100.0,
                    "Body_Temp": 37.5
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/predict",
            json=out_of_range_data
        )
        
        # This might return 200 or 500 depending on how the model handles it
        # But it shouldn't crash the service
        self.assertIn(response.status_code, [200, 500])


if __name__ == "__main__":
    # Change to the calorie_prediction_v1 directory
    os.chdir("calorie_prediction_v1")
    
    # Run the tests
    unittest.main()