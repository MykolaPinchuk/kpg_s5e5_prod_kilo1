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
    'Duration': 200.0,
    'Heart_Rate': 100.0,
    'Body_Temp': 37.5
}])
print(f'Raw payload: {sample_data}')

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

print(f'X: {X}')
print(f"Predicted calories burned: {prediction[0]:.2f}")