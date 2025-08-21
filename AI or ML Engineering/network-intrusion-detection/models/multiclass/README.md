# Multiclass Cybersecurity Intrusion Detection Model - Deployment Guide

## Model Information
- **Algorithm**: GradientBoosting Classifier
- **Training Date**: 20250807_050327
- **Test Weighted F1-Score**: 80.2376
- **Test Accuracy**: 79.0461
- **Test Macro F1**: 55.1555
- **Training Time**: 1366.83 seconds

## Dataset Information
- **Training Samples**: 149,585 (after multi-tier rebalancing)
- **Test Samples**: 45,328
- **Features**: 63 (after preprocessing)
- **Classes**: 9 attack categories

## Attack Categories
- Analysis
- Backdoor
- DoS
- Exploits
- Fuzzers
- Generic
- Reconnaissance
- Shellcode
- Worms

## Files in this directory:
1. `multiclass_gradientboosting_model.joblib` - Main GradientBoosting model
2. `multiclass_target_encoder.pkl` - Target encoder untuk categorical features
3. `label_encoder.pkl` - Label encoder untuk target classes
4. `preprocessor.joblib` - Data preprocessor (scaler + encoder)
5. `feature_config.json` - Feature configuration dan metadata
6. `README.md` - This deployment guide

## Usage for New Predictions:
```python
import joblib
import pickle
import pandas as pd

# Load components
model = joblib.load('multiclass_extratrees_model.joblib')
with open('multiclass_target_encoder.pkl', 'rb') as f:
    target_encoder = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
preprocessor = joblib.load('preprocessor.joblib')

# Prepare new data
# ... (encode categorical features, preprocess, predict)
```

## Important Notes:
- Model trained dengan multi-tier rebalancing strategy
- Uses probability-based target encoding untuk categorical features
- Preprocessor must be applied dalam urutan yang sama
- All categorical features harus di-encode sebelum preprocessing
- Model expects features dalam urutan yang sama seperti training data
