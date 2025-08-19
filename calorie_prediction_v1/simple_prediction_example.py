"""
Simple example script demonstrating how to manually pass a payload and receive a prediction value.

This script shows the minimal steps required to:
1. Load a pre-trained model
2. Accept a simple input payload
3. Preprocess the data
4. Generate features
5. Make a prediction
6. Return the prediction value

This is a simplified version without abstraction layers to make it easy to see how raw payloads 
are converted to predictions.
"""

import pandas as pd
import joblib
import numpy as np

# Import the preprocessing and feature engineering functions
from src.data_preprocessing import preprocess_data
from src.feature_engineering import create_essential_features, get_feature_columns
from src.model_pipeline import load_model


def manual_prediction_example():
    """
    Simple example of making a prediction with a manually created payload.
    """
    print("=== Simple Prediction Example ===\n")
    
    # Step 1: Load the pre-trained model
    print("1. Loading pre-trained model...")
    model, metadata = load_model('models/baseline_xgb_model.pkl')
    print(f"   Model loaded successfully!")
    print(f"   Model type: {type(model)}")
    print(f"   Feature type used in training: {metadata.get('feature_type', 'essential')}")
    print()
    
    # Step 2: Accept a simple input payload (dictionary with required features)
    print("2. Creating input payload...")
    # Example payload - this is what a user would provide as raw input
    payload = {
        'id': 1,
        'Gender': 'male',  # or 'female'
        'Age': 30,
        'Height': 175.0,   # in cm
        'Weight': 70.0,    # in kg
        'Duration': 30.0,  # in minutes
        'Heart_Rate': 100.0,  # in bpm
        'Body_Temp': 37.5   # in Celsius
    }
    print(f"   Input payload: {payload}")
    print()
    
    # Step 3: Preprocess the data
    print("3. Preprocessing data...")
    # Convert payload to DataFrame (simulating how raw data would be loaded)
    raw_df = pd.DataFrame([payload])
    print(f"   Raw data shape: {raw_df.shape}")
    print(f"   Raw data columns: {list(raw_df.columns)}")
    
    # Apply preprocessing (handles missing values, categorical encoding, etc.)
    processed_df = preprocess_data(raw_df)
    print(f"   Processed data shape: {processed_df.shape}")
    print(f"   Processed data columns: {list(processed_df.columns)}")
    print()
    
    # Step 4: Generate features
    print("4. Generating features...")
    # Create essential features (same as used in training)
    features_df, new_features = create_essential_features(processed_df)
    print(f"   Features data shape: {features_df.shape}")
    print(f"   New features created: {new_features}")
    print(f"   Total features: {len(get_feature_columns(features_df))}")
    print()
    
    # Step 5: Make a prediction
    print("5. Making prediction...")
    # Get the feature columns that the model expects
    feature_columns = get_feature_columns(features_df)
    print(f"   Using {len(feature_columns)} features for prediction")
    
    # Prepare the data for prediction (same columns and order as training)
    X = features_df[feature_columns]
    print(f"   Prediction input shape: {X.shape}")
    
    # Make the prediction
    prediction = model.predict(X)
    print(f"   Raw prediction: {prediction}")
    print()
    
    # Step 6: Return the prediction value
    print("6. Returning prediction value...")
    # The prediction is in calories
    calories_predicted = float(prediction[0])
    print(f"   Predicted calories burned: {calories_predicted:.2f} calories")
    print()
    
    return calories_predicted


def multiple_predictions_example():
    """
    Example with multiple data points.
    """
    print("=== Multiple Predictions Example ===\n")
    
    # Load the model
    model, metadata = load_model('models/baseline_xgb_model.pkl')
    
    # Create multiple payloads
    payloads = [
        {
            'id': 1,
            'Gender': 'male',
            'Age': 25,
            'Height': 180.0,
            'Weight': 75.0,
            'Duration': 45.0,
            'Heart_Rate': 120.0,
            'Body_Temp': 38.0
        },
        {
            'id': 2,
            'Gender': 'female',
            'Age': 35,
            'Height': 165.0,
            'Weight': 60.0,
            'Duration': 30.0,
            'Heart_Rate': 100.0,
            'Body_Temp': 37.0
        },
        {
            'id': 3,
            'Gender': 'male',
            'Age': 45,
            'Height': 170.0,
            'Weight': 85.0,
            'Duration': 20.0,
            'Heart_Rate': 90.0,
            'Body_Temp': 37.5
        }
    ]
    
    print(f"Making predictions for {len(payloads)} data points...")
    
    # Convert to DataFrame
    raw_df = pd.DataFrame(payloads)
    print(f"Raw data shape: {raw_df.shape}")
    
    # Preprocess
    processed_df = preprocess_data(raw_df)
    print(f"Processed data shape: {processed_df.shape}")
    
    # Generate features
    features_df, new_features = create_essential_features(processed_df)
    print(f"Features data shape: {features_df.shape}")
    
    # Get feature columns
    feature_columns = get_feature_columns(features_df)
    X = features_df[feature_columns]
    
    # Make predictions
    predictions = model.predict(X)
    
    # Display results
    print("\nPredictions:")
    for i, (payload, pred) in enumerate(zip(payloads, predictions)):
        print(f"  Person {i+1}: {pred:.2f} calories (Age: {payload['Age']}, Gender: {payload['Gender']}, Duration: {payload['Duration']} min)")
    
    return predictions


if __name__ == "__main__":
    # Run the simple example
    single_prediction = manual_prediction_example()
    
    print("=" * 50)
    print()
    
    # Run the multiple predictions example
    multiple_predictions = multiple_predictions_example()
    
    print("\n=== Examples completed! ===")