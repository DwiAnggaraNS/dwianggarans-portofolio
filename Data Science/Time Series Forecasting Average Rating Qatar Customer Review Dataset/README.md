## Time Series Forecasting Average Rating Qatar Customer Review Dataset 🏆

**🥇 1st Place Winner - Falcon x Qatar Airways AI Infographic Competition**  
*By Team MelangkahDariTengah: Dwi Anggara Najwan Sugama*

Advanced time series analysis and forecasting model for predicting Qatar Airways customer satisfaction trends. This predictive analysis was instrumental in creating the award-winning infographic "Warning Signs in the Skies" 📈

## Competition Achievement 🏅

**Competition:** Falcon x Qatar Airways AI Infographic Competition  
**Result:** 🥇 1st Place out of 12 national finalists (from 57+ teams)  
**Date:** November 2024  
**Awarded by:** Universitas Pelita Harapan (UPH) & Qatar Airways  
**Infographic:** [View Winner Infographic](https://drive.google.com/file/d/1nPFPq7h0SvCGwUQta0J9imdgftsx0PFK/view?usp=sharing) 🎨

## Project Overview 🎯

This notebook implements comprehensive time series forecasting techniques to predict future customer satisfaction ratings for Qatar Airways. The analysis transforms historical customer review data into actionable predictive insights, enabling proactive service quality management.

### Key Achievements 💡
- **Temporal Pattern Recognition**: Identified seasonal and trending patterns in customer satisfaction
- **Predictive Modeling**: Built robust forecasting models using multiple machine learning algorithms
- **Data-Driven Insights**: Generated forward-looking recommendations for service improvement
- **Risk Prediction**: Early warning system for potential satisfaction declines

## Features 🔍

### Time Series Analysis Components
- **Data Preprocessing**: Conversion to monthly aggregated rating averages
- **Temporal Feature Engineering**: Date-based feature extraction and trend analysis
- **Missing Value Handling**: Linear interpolation for data continuity
- **Multi-Model Ensemble**: Comprehensive algorithm comparison and selection

### Machine Learning Pipeline
- **Multiple Algorithms**: RandomForest, XGBoost, LightGBM, Linear models, SVM, Neural Networks
- **Advanced Preprocessing**: StandardScaler, RobustScaler, MinMaxScaler optimization
- **Model Evaluation**: MSE-based performance comparison and validation
- **Hyperparameter Optimization**: Grid search and cross-validation

## Technical Stack 🛠️

```python
# Core Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Machine Learning
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# Preprocessing & Evaluation
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
```

## Dataset Information 📊

**Source:** Qatar Airways Customer Reviews (Time Series)  
**URL:** [GitHub Repository](https://raw.githubusercontent.com/DwiAnggaraNS/AI-MelangkahDariTengah-2024/main/Airline_Qatar_Reviews.csv)  
**Processing:**
- Monthly aggregation of customer ratings
- Linear interpolation for missing values
- Chronological sorting and indexing
- Feature engineering for temporal patterns

## Methodology 🔬

### Data Preprocessing Pipeline
1. **Date Conversion**: Parse and standardize date formats
2. **Monthly Resampling**: Aggregate ratings by month for trend analysis
3. **Missing Value Treatment**: Linear interpolation for data continuity
4. **Feature Engineering**: Create temporal features (month, quarter, year trends)

### Model Development Process
1. **Algorithm Selection**: Test 10+ regression algorithms
2. **Preprocessing Optimization**: Compare multiple scaling techniques
3. **Performance Evaluation**: MSE-based model comparison
4. **Ensemble Methods**: Combine best-performing models
5. **Validation**: Time-based cross-validation for temporal data

### Forecasting Techniques
- **Traditional ML**: Random Forest, Gradient Boosting, XGBoost
- **Linear Models**: Ridge, Lasso, ElasticNet regression
- **Advanced Methods**: SVM, KNN, Kernel Ridge
- **Deep Learning**: Neural network architectures

## Key Insights 📈

### Temporal Patterns Discovered
- **Seasonal Variations**: Identified recurring satisfaction patterns
- **Trend Analysis**: Long-term customer satisfaction trajectories
- **Anomaly Detection**: Unusual rating periods requiring investigation
- **Predictive Indicators**: Early warning signals for satisfaction decline

### Business Impact
- **Proactive Management**: Anticipate satisfaction issues before they occur
- **Resource Allocation**: Data-driven decision making for service improvements
- **Strategic Planning**: Long-term service quality roadmap development
- **Competitive Advantage**: Predictive insights for market positioning

## Usage Instructions 🚀

### Environment Setup
```bash
# Install required packages
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm
```

### Running the Analysis
```bash
# Execute the notebook
jupyter notebook ModelingTimeSeriesRating_MelangkahDariTengah.ipynb
```

### Analysis Workflow
1. **Data Loading**: Import and preprocess time series data
2. **Exploratory Analysis**: Visualize temporal patterns
3. **Model Training**: Train multiple forecasting algorithms
4. **Performance Evaluation**: Compare model accuracies
5. **Prediction Generation**: Create future satisfaction forecasts

## Model Performance 🎯

### Evaluation Metrics
- **Primary Metric**: Mean Squared Error (MSE)
- **Model Comparison**: Comprehensive algorithm benchmarking
- **Validation Strategy**: Time-based train/validation split
- **Feature Importance**: Analysis of predictive factors

### Best Performing Models
Results vary based on dataset characteristics, but typical top performers include:
- **Ensemble Methods**: Random Forest, Gradient Boosting
- **Advanced ML**: XGBoost, LightGBM
- **Linear Models**: Ridge Regression (for interpretability)

## Competition Impact 🌟

This time series analysis contributed to the winning submission by:
- **Predictive Insights**: Forward-looking customer satisfaction trends
- **Data Visualization**: Compelling temporal trend visualizations
- **Strategic Recommendations**: Proactive service improvement suggestions
- **Quantitative Evidence**: Statistical backing for infographic claims

## Future Enhancements 🔮

- [ ] **Deep Learning Models**: LSTM, GRU, Transformer architectures
- [ ] **Multivariate Analysis**: Include external factors (seasonality, events)
- [ ] **Real-time Forecasting**: Live prediction system integration
- [ ] **Confidence Intervals**: Uncertainty quantification for predictions
- [ ] **Automated Retraining**: Model updates with new data

## Files Structure 📁

```
Time Series Forecasting Average Rating Qatar Customer Review Dataset/
├── ModelingTimeSeriesRating_MelangkahDariTengah.ipynb  # Main forecasting notebook
└── README.md                                           # This documentation
```

## Author 👨‍💻

**Dwi Anggara Najwan Sugama**  
*Competition Winner & Time Series Analytics Expert*  
Team MelangkahDariTengah

---

*This project demonstrates the application of advanced time series forecasting techniques to airline industry challenges, providing predictive insights that enable proactive customer satisfaction management.* ✨

## License 📄

Academic and Educational Use
