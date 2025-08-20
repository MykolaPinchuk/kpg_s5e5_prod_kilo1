# Calorie Expenditure Model v1 - Containerized Application

## Overview
This is version 1 of the calorie expenditure prediction model, implemented as a containerized application using FastAPI. This version builds upon the v0 implementation by adding a REST API interface and Docker containerization for easier deployment.

## New Features in v1
- **FastAPI REST API**: Exposes the model through a RESTful interface
- **Containerization**: Docker image for consistent deployment across environments
- **Configuration Management**: YAML-based configuration for model parameters
- **Health Checks**: API endpoints for monitoring service status

## File Structure
```
calorie_prediction_v1/
├── api/                          # API interface layer
│   ├── app.py                   # FastAPI application
│   ├── routes.py                # API endpoints
│   └── models.py                # Request/response models
├── config/                       # Configuration files
│   └── model_config.yaml        # Model configuration
├── data/                         # Data handling
│   ├── train_subsample.csv      # Training data (10% sample)
│   └── test_subsample.csv       # Test data (10% sample)
├── models/                       # Model files
│   └── baseline_xgb_model.pkl   # Pre-trained XGBoost model
├── src/                          # Core pipeline code
│   ├── __init__.py              # Package initialization
│   ├── data_preprocessing.py    # Data cleaning and validation
│   ├── feature_engineering.py   # Feature creation utilities
│   └── model_pipeline.py        # Training/inference pipeline
├── tests/                        # Test suite
│   ├── test_docker.py           # Docker build tests
│   └── run_tests.py             # Docker-based test runner
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Development orchestration
├── .dockerignore                 # Docker ignore file
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── DEPLOYMENT_SUMMARY.md         # Technical summary
```

## API Endpoints
- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - Health check endpoint
- `POST /api/v1/predict` - Prediction endpoint for calorie expenditure

## Setup Instructions

### Prerequisites
- Python 3.11 (specifically)
- pip package manager
- Docker (optional, for containerized deployment)

### Checking Your Python Version
Before setting up the environment, verify your Python version:

```bash
python3 --version
# or
python --version
```

If you see Python 3.11.x, you're good to proceed. If not, follow the installation instructions below.

### Installing Python 3.11
If Python 3.11 is not installed on your system, follow these platform-specific instructions:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**macOS (using Homebrew):**
```bash
brew install python@3.11
```

**Windows:**
1. Download Python 3.11 from the official Python website: https://www.python.org/downloads/
2. Run the installer and make sure to check "Add Python to PATH"

### Setting Up a Virtual Environment
It's recommended to use a virtual environment to avoid conflicts with other Python projects. To create a virtual environment specifically with Python 3.11:

```bash
# Create a virtual environment using Python 3.11 specifically
python3.11 -m venv venv
# or if python3.11 is not available in PATH:
/usr/bin/python3.11 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Installing Dependencies
Once your virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:
- pandas==2.0.3
- scikit-learn==1.5.1
- xgboost==2.0.3
- numpy==1.24.4
- fastapi==0.110.0
- uvicorn==0.29.0
- pyyaml==6.0.1

## Running the Application

### Using Docker (Recommended)
1. Build the Docker image:
   ```bash
   docker build -t calorie-prediction-api .
   ```

2. Run the container:
   ```bash
   sudo docker run -p 8000:8000 calorie-prediction-api
   ```

3. Access the API at `http://localhost:8000`

### Using Docker Compose
1. Start the service:
   ```bash
   docker-compose up
   ```

2. Access the API at `http://localhost:8000`


## Testing

### Running Tests with Docker (Recommended)
When Docker is available, you can run the full test suite including Docker-specific tests:

```bash
# Make sure you're in the calorie_prediction_v1 directory
cd calorie_prediction_v1

# Run all tests including Docker tests
python -m tests.run_tests
```

Run specific Docker tests:
```bash
# Test Docker build specifically
python -m tests.test_docker
```


## API Usage Examples

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Prediction Request
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "workouts": [
      {
        "id": "workout1",
        "Gender": "male",
        "Age": 30,
        "Height": 175.0,
        "Weight": 70.0,
        "Duration": 30.0,
        "Heart_Rate": 100.0,
        "Body_Temp": 37.5
      }
    ]
  }'
```


## Configuration
The application can be configured using the `config/model_config.yaml` file:
- Model path and parameters
- API settings (host, port, etc.)
- Feature engineering options
- Validation rules

## Notes
- The containerized application exposes port 8000 by default
- Data and model files are mounted as volumes in Docker Compose
- The API supports both single and batch predictions
- Input validation is performed on all requests
