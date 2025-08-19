"""
Main FastAPI application for the calorie prediction service.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import yaml

from .routes import router as prediction_router

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

# Create FastAPI app
app = FastAPI(
    title="Calorie Expenditure Prediction API",
    description="API for predicting calorie expenditure based on workout data",
    version=config.get('model', {}).get('version', '1.0.0')
)

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """
    Initialize resources when the application starts.
    """
    logger.info("Starting calorie prediction API...")
    # Any initialization code can go here
    logger.info("API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up resources when the application shuts down.
    """
    logger.info("Shutting down calorie prediction API...")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Calorie Expenditure Prediction API",
        "version": config.get('model', {}).get('version', '1.0.0'),
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    # Get port from configuration or environment variable or default to 8000
    port = int(os.environ.get("PORT", config.get('api', {}).get('port', 8000)))
    
    # Run the application
    uvicorn.run(
        "api.app:app",
        host=config.get('api', {}).get('host', "0.0.0.0"),
        port=port,
        reload=config.get('api', {}).get('reload', False),
        log_level=config.get('api', {}).get('log_level', "info")
    )