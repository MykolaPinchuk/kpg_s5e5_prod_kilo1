"""
API routes for the calorie prediction service.
"""
import pandas as pd
from fastapi import APIRouter, HTTPException
from typing import List
import os
import sys
import logging
import yaml

# Add the src directory to the path so we can import the model pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model_pipeline import load_model, predict
from api.models import WorkoutData, PredictionRequest, PredictionResponse, HealthCheckResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'model_config.yaml')
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Failed to load configuration: {str(e)}")
    config = {}

# Create router
router = APIRouter()

# Global model variable
model = None
feature_type = config.get('model', {}).get('feature_type', 'essential')  # Must match the training configuration


def initialize_model():
    """
    Initialize the model when the application starts.
    """
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', config.get('model', {}).get('path', 'models/baseline_xgb_model.pkl'))
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        model, metadata = load_model(model_path)
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


def convert_workouts_to_dataframe(workouts: List[WorkoutData]) -> pd.DataFrame:
    """
    Convert a list of WorkoutData objects to a pandas DataFrame.
    
    Args:
        workouts: List of WorkoutData objects
        
    Returns:
        pd.DataFrame: DataFrame with workout data
    """
    # Convert to list of dictionaries
    data = []
    for workout in workouts:
        workout_dict = workout.dict()
        # Handle Gender field (convert to Sex if needed by preprocessing)
        if 'Gender' in workout_dict and workout_dict['Gender'] is not None:
            workout_dict['Sex'] = workout_dict.pop('Gender')
        data.append(workout_dict)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return HealthCheckResponse(
        status="healthy",
        version=config.get('model', {}).get('version', '1.0.0')
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_calories(request: PredictionRequest):
    """
    Predict calorie expenditure for workout sessions.
    
    Args:
        request: PredictionRequest with workout data
        
    Returns:
        PredictionResponse with predictions
    """
    global model
    
    # Initialize model if not already loaded
    if model is None:
        try:
            model = initialize_model()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Model initialization failed: {str(e)}"
            )
    
    try:
        # Convert workouts to DataFrame
        workout_df = convert_workouts_to_dataframe(request.workouts)
        
        # Add a dummy Calories column for validation (not used in prediction)
        workout_df['Calories'] = 0
        
        # Save DataFrame to temporary CSV for processing
        temp_csv_path = "/tmp/workout_data.csv"
        workout_df.to_csv(temp_csv_path, index=False)
        
        # Make predictions using the model pipeline
        prediction_results = predict(
            model=model,
            test_data_path=temp_csv_path,
            feature_type=feature_type
        )
        
        # Clean up temporary file
        os.remove(temp_csv_path)
        
        # Format response
        response = PredictionResponse(
            predictions=prediction_results['predictions'].tolist(),
            workout_ids=prediction_results['test_ids'].tolist(),
            prediction_metadata={
                'num_samples': prediction_results['num_samples'],
                'prediction_range': prediction_results['prediction_range']
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )