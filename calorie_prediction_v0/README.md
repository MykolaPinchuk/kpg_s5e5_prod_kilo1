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
files_for_deployment/
├── README.md                    # This file
├── data/
│   ├── train_subsample.csv     # Training data (10% sample)
│   └── test_subsample.csv      # Test data (10% sample)
├── models/
│   └── baseline_xgb_model.pkl  # Trained XGBoost model
├── src/
│   ├── model_pipeline.py       # Complete training/inference pipeline
│   └── feature_engineering.py  # Feature creation utilities
└── requirements.txt            # Python dependencies

```

## Quick Start
```python
# Load and use the model
import joblib
from src.model_pipeline import preprocess_and_predict

# Load trained model
model = joblib.load('models/baseline_xgb_model.pkl')

# Make predictions on new data
predictions = preprocess_and_predict(model, new_data)
```

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
