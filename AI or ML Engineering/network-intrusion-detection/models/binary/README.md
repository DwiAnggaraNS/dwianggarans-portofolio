# Cybersecurity Intrusion Detection Model - Deployment Guide

## Model Information
- **Algorithm**: Random Forest Classifier
- **Training Date**: 20250727_102511
- **F1-Score**: 0.917175  
- **AUC**: 0.984348  
- **Recall**: 0.976749
  
## Files in this directory:
1. `main_model.joblib` - Complete trained pipeline
2. `target_encoder.pkl` - Target encoder for 'proto' feature
3. `feature_config.json` - Feature configuration and metadata
4. `README.md` - This deployment guide

## Usage for New Predictions:
```python
import joblib
import pickle
import pandas as pd

# Load components
model = joblib.load('main_model.joblib')
with open('target_encoder.pkl', 'rb') as f:
    target_encoder = pickle.load(f)

# Prepare new data
# ... (see example in notebook)
```

## Important Notes:
- Always encode 'proto' feature using the saved target_encoder
- Ensure all required features are present in the input data
- Model expects the same feature order as training data
