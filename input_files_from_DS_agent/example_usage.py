"""
Example usage of the calorie expenditure prediction pipeline.
Demonstrates training, inference, and submission generation.
"""
import os
from src.model_pipeline import train_model, predict, load_model, create_submission

# Example 1: Train a new baseline model
def train_baseline_example():
    """Train a baseline XGBoost model with essential features."""
    print("Training baseline model...")
    
    results = train_model(
        train_data_path='data/train_subsample.csv',
        model_type='baseline',
        feature_type='essential',
        test_size=0.2,
        validation_size=0.2,
        random_state=42
    )
    
    print(f"Training completed!")
    print(f"Validation RMSLE: {results['metrics']['val_rmsle']:.4f}")
    print(f"Test RMSLE: {results['metrics']['test_rmsle']:.4f}")
    print(f"Overfitting ratio: {results['metrics']['overfitting_ratio']:.4f}")
    print(f"Features used: {len(results['feature_columns'])}")
    print(f"New features created: {results['new_features']}")
    
    return results


# Example 2: Use pre-trained model for inference
def inference_example():
    """Make predictions using the pre-trained model."""
    print("Loading pre-trained model...")
    
    # Load the trained model
    model, metadata = load_model('models/baseline_xgb_model.pkl')
    
    # Make predictions on test data
    prediction_results = predict(
        model=model,
        test_data_path='data/test_subsample.csv',
        feature_type='essential'  # Must match training
    )
    
    print(f"Predictions completed!")
    print(f"Number of predictions: {prediction_results['num_samples']}")
    print(f"Prediction range: {prediction_results['prediction_range']['min']:.1f} - {prediction_results['prediction_range']['max']:.1f}")
    print(f"Mean prediction: {prediction_results['prediction_range']['mean']:.1f}")
    
    return prediction_results


# Example 3: Create submission file
def submission_example():
    """Create a Kaggle submission file."""
    print("Creating submission file...")
    
    # Load the trained model
    model, metadata = load_model('models/baseline_xgb_model.pkl')
    
    # Create submission
    submission_df = create_submission(
        model=model,
        test_data_path='data/test_subsample.csv',
        submission_path='submission.csv',
        feature_type='essential'
    )
    
    print(f"Submission created with {len(submission_df)} predictions")
    print(f"Saved to: submission.csv")
    
    return submission_df


if __name__ == "__main__":
    # Run examples
    print("=== Calorie Expenditure Model Pipeline Examples ===\n")
    
    # Example 1: Training (uncomment to train new model)
    # train_results = train_baseline_example()
    
    # Example 2: Inference with pre-trained model
    predictions = inference_example()
    
    # Example 3: Create submission
    submission = submission_example()
    
    print("\n=== Examples completed! ===")