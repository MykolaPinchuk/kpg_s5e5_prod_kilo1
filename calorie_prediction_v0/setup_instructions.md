# Setup Instructions for Calorie Prediction Model

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Setup Steps

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Linux/macOS:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

After setting up the environment, you can run the tests:

```bash
python -m tests.run_tests
```

Or run individual test files:
```bash
python -m tests.test_model_loading
python -m tests.test_inference
python -m tests.test_data_preprocessing
python -m tests.test_feature_engineering
```

## Using the Model

After setting up the environment, you can use the model:

```bash
python example_usage.py
```

This will run the example usage script that demonstrates how to:
- Load the pre-trained model
- Make predictions on test data
- Create a submission file