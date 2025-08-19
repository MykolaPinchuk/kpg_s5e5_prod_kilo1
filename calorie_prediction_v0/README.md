# Calorie Expenditure Model Deployment Package

## Overview
This package contains the essential files for deploying the baseline XGBoost model for calorie expenditure prediction in a production environment. The model was trained on the Kaggle Playground Series S5E5 competition data.

## Problem Description
- **Task**: Regression - predict calorie expenditure during workouts
- **Features**: Gender, Age, Height, Weight, Duration, Heart_Rate, Body_Temp
- **Target**: Calories burned (continuous variable)
- **Metric**: RMSLE (Root Mean Squared Logarithmic Error)

## Model Performance
- **Validation RMSLE**: ~0.07 (baseline XGBoost)
- **Training Time**: <3 seconds
- **Model Size**: ~157KB

## File Structure
```
calorie_prediction_v0/
├── README.md                    # This file
├── data/
│   ├── train_subsample.csv     # Training data (10% sample)
│   └── test_subsample.csv      # Test data (10% sample)
├── models/
│   └── baseline_xgb_model.pkl  # Trained XGBoost model
├── src/
│   ├── __init__.py             # Package initialization
│   ├── data_preprocessing.py   # Data cleaning and validation
│   ├── feature_engineering.py  # Feature creation utilities
│   └── model_pipeline.py       # Complete training/inference pipeline
├── tests/
│   ├── run_tests.py            # Test runner script
│   ├── test_model_loading.py   # Tests for model loading
│   ├── test_inference.py       # Tests for inference functionality
│   ├── test_data_preprocessing.py # Tests for data preprocessing
│   └── test_feature_engineering.py # Tests for feature engineering
├── requirements.txt            # Python dependencies
├── example_usage.py            # Usage examples
├── simple_prediction_example.py # Simple prediction example
├── setup_instructions.md       # Setup instructions
└── setup.sh                    # Setup script

```

## Quick Start
```python
# Load and use the model
from src.model_pipeline import load_model, predict

# Load trained model
model, metadata = load_model('models/baseline_xgb_model.pkl')

# Make predictions on test data
results = predict(model, 'data/test_subsample.csv', feature_type='essential')

# Print prediction statistics
print(f"Number of predictions: {results['num_samples']}")
print(f"Mean prediction: {results['prediction_range']['mean']:.2f} calories")
```

For more detailed examples, see the "Testing the Model" section below or run:
```bash
python example_usage.py
```

## Testing the Model

This section explains how to test the v0 implementation of the calorie prediction model.

### 1. Setting Up the Environment

You can either use the existing virtual environment or create a new one:

**Option A: Using the existing virtual environment (recommended)**
```bash
# Activate the existing virtual environment
source venv311/bin/activate
```

**Option B: Creating a new virtual environment**
```bash
# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt
```

### 2. Running Tests

**Run all tests:**
```bash
python -m tests.run_tests
```

**Run individual test files:**
```bash
# Test model loading
python -m tests.test_model_loading

# Test inference functionality
python -m tests.test_inference

# Test data preprocessing
python -m tests.test_data_preprocessing

# Test feature engineering
python -m tests.test_feature_engineering
```

### 3. Running Example Scripts

**Run the simple prediction example script:**
```bash
python simple_prediction_example.py
```

**Run the original example usage script:**
```bash
python example_usage.py
```

### 4. Manual Testing with Python

You can manually test the model using Python:

```python
# Load the model
from src.model_pipeline import load_model
model, metadata = load_model('models/baseline_xgb_model.pkl')

# Create sample data for prediction
import pandas as pd
sample_data = pd.DataFrame([{
    'id': 1,
    'Gender': 'male',
    'Age': 30,
    'Height': 175.0,
    'Weight': 70.0,
    'Duration': 30.0,
    'Heart_Rate': 100.0,
    'Body_Temp': 37.5
}])

# Preprocess the data
from src.data_preprocessing import preprocess_data
processed_data = preprocess_data(sample_data)

# Create features
from src.feature_engineering import create_essential_features, get_feature_columns
features_data, _ = create_essential_features(processed_data)

# Get feature columns and make prediction
feature_columns = get_feature_columns(features_data)
X = features_data[feature_columns]
prediction = model.predict(X)

print(f"Predicted calories burned: {prediction[0]:.2f}")
```

### 5. Expected Test Results

When running the tests, you should expect:
- All tests to pass without errors
- Test output showing successful execution of test cases
- No failures or errors in the test suite

Example successful test output:
```
Running all tests...
test_model_file_exists (__main__.TestModelLoading) ... ok
test_load_model_success (__main__.TestModelLoading) ... ok
test_model_metadata (__main__.TestModelLoading) ... ok
...

----------------------------------------------------------------------
Ran X tests in X.XXXs

OK
```

### 6. Troubleshooting Tips

**Common issues and solutions:**

1. **Missing dependencies:**
   - Ensure all packages in `requirements.txt` are installed
   - Run `pip install -r requirements.txt`

2. **Import errors:**
   - Make sure you're running commands from the `calorie_prediction_v0` directory
   - Check that the virtual environment is activated

3. **Model loading errors:**
   - Verify that `models/baseline_xgb_model.pkl` exists
   - Check file permissions

4. **Data file errors:**
   - Ensure `data/train_subsample.csv` and `data/test_subsample.csv` exist
   - Check file permissions

5. **Python path issues:**
   - Make sure you're using Python 3.8 or higher
   - Ensure the `src` directory is in your Python path

6. **Virtual environment issues:**
   - If you can't create a virtual environment, try using the existing `venv311`
   - On some systems, you might need to install `python3-venv` package

## Features Created
The model uses 7 essential engineered features:
1. BMI (Body Mass Index)
2. Duration_HR_interaction 
3. Weight_HR_interaction
4. MET_estimated (metabolic equivalent estimation)
5. MET_Duration_product
6. Temp_deviation (deviation from normal body temp)
7. Duration_HR_Temp_interaction (triple interaction)


## Broad context
Competition: Predict Calorie Expenditure (Playground Series - Season 5, Episode 5)
The goal of this competition is to predict the number of calories burned during a workout. This is a regression problem where you will predict a continuous target value. Data is organized at a workout level. Thus the business goal of this model is to predict for each workout features (assumed to come in near real time) calorie expenditure.

To simulate production-like environment, we may want to simulate real-time data feed. One way to do it is to resample observations from a train set, either raw or altered.

## Notes
We want to deploy this locally. Cloud deployment is out of scope. For the final version of deployment, we want to follow best practices whever they make sense for this project. We do not want to overengineer.


## Dependencies
- pandas==2.0.3
- scikit-learn==1.5.1  
- xgboost==2.0.3
- numpy==1.24.4

Total lines of code: <1000 (excluding data files)
