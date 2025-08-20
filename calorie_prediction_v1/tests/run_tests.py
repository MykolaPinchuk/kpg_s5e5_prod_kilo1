"""
Test runner for calorie prediction v1 implementation.
Only runs Docker-based tests as direct implementation has been removed.
"""
import unittest
import sys
import os

# Add the current directory to the path so we can import test modules
sys.path.insert(0, os.path.dirname(__file__))
# Add the parent directory to the path so we can import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def is_docker_available():
    """
    Check if Docker is available on the system.
    
    Returns:
        bool: True if Docker is available, False otherwise.
    """
    try:
        import subprocess
        # Try to run a simple Docker command
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False

def run_tests():
    """Run Docker-based tests for the calorie prediction API."""
    print("Running Docker-based tests for Calorie Prediction API v1...")
    print("=" * 50)
    
    # Check if Docker is available
    if not is_docker_available():
        print("Docker is not available. Skipping Docker tests.")
        print("To run Docker tests, please install Docker and ensure it's running.")
        return 0
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Only add Docker tests since direct implementation has been removed
    try:
        from test_docker import TestDockerBuild
        suite.addTests(loader.loadTestsFromTestCase(TestDockerBuild))
        print("Docker tests loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load Docker tests: {e}")
        return 1
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)