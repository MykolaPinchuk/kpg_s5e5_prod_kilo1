"""
Test suite for Docker image build and basic functionality.
"""
import unittest
import subprocess
import os
import sys

# Add the tests directory to the path so we can import test utilities
sys.path.insert(0, os.path.dirname(__file__))

try:
    from test_utils import is_docker_available, skip_if_no_docker
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
    
    def skip_if_no_docker():
        def decorator(test_func):
            if not is_docker_available():
                return unittest.skip("Docker is not available")(test_func)
            return test_func
        return decorator

class TestDockerBuild(unittest.TestCase):
    """Test cases for Docker image build."""
    
    def setUp(self):
        """Set up test environment."""
        self.project_dir = "calorie_prediction_v1"
    
    @skip_if_no_docker()
    def test_docker_build_success(self):
        """Test that Docker image builds successfully."""
        try:
            result = subprocess.run(
                ["docker", "build", "-t", "calorie-prediction-api", "."],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            self.assertEqual(
                result.returncode, 0,
                f"Docker build failed with output:\n{result.stdout}\n{result.stderr}"
            )
            
            print("Docker image built successfully")
            
        except subprocess.TimeoutExpired:
            self.fail("Docker build timed out")
        except FileNotFoundError:
            self.fail("Docker is not installed or not in PATH")
        except Exception as e:
            self.fail(f"Docker build failed with exception: {str(e)}")
    
    @skip_if_no_docker()
    def test_docker_image_exists(self):
        """Test that the Docker image exists after build."""
        # First build the image
        build_result = subprocess.run(
            ["docker", "build", "-t", "calorie-prediction-api", "."],
            cwd=self.project_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(build_result.returncode, 0, "Docker build failed")
        
        # Check if image exists
        result = subprocess.run(
            ["docker", "images", "calorie-prediction-api", "--format", "table"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, "Failed to list Docker images")
        self.assertIn("calorie-prediction-api", result.stdout, "Docker image not found")
        
        print("Docker image exists")


if __name__ == "__main__":
    unittest.main()