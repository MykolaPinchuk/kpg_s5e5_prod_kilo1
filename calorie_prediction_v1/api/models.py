"""
Pydantic models for request/response validation in the calorie prediction API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd


class WorkoutData(BaseModel):
    """
    Input data for a single workout session.
    """
    id: str = Field(..., description="Unique identifier for the workout")
    Gender: Optional[str] = Field(None, description="Gender of the person (male/female)")
    Age: int = Field(..., ge=10, le=100, description="Age in years")
    Height: float = Field(..., ge=100, le=250, description="Height in cm")
    Weight: float = Field(..., ge=30, le=200, description="Weight in kg")
    Duration: float = Field(..., ge=0, le=300, description="Workout duration in minutes")
    Heart_Rate: float = Field(..., ge=50, le=220, description="Average heart rate during workout (bpm)")
    Body_Temp: float = Field(..., ge=35, le=42, description="Average body temperature during workout (°C)")


class PredictionRequest(BaseModel):
    """
    Request model for making calorie predictions.
    Can handle single or batch predictions.
    """
    workouts: List[WorkoutData] = Field(..., description="List of workout data for prediction")


class PredictionResponse(BaseModel):
    """
    Response model for calorie predictions.
    """
    predictions: List[float] = Field(..., description="Predicted calorie expenditures")
    workout_ids: List[str] = Field(..., description="Corresponding workout IDs")
    prediction_metadata: dict = Field(..., description="Metadata about the predictions")


class HealthCheckResponse(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str = Field(..., description="Health status of the service")
    version: str = Field(..., description="API version")