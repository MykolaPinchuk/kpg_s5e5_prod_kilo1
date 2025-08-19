"""
Utility functions for tests.
"""
import subprocess
import unittest


def is_docker_available():
    """
    Check if Docker is available on the system.
    
    Returns:
        bool: True if Docker is available, False otherwise.
    """
    try:
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


def skip_if_no_docker():
    """
    Decorator to skip tests if Docker is not available.
    
    Returns:
        function: A decorator function.
    """
    def decorator(test_func):
        if not is_docker_available():
            return unittest.skip("Docker is not available")(test_func)
        return test_func
    return decorator