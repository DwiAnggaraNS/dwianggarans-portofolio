# 🏆 HaloRek - Credit Card Approval Classification Website

**🥇 First Place Winner - Data Science ICONIC IT Competition**  
*By Team HaloRek: Dwi Anggara N.S, Muhammad Natha Ulinnuha, Naufal Afif Bauw*

A competition-winning machine learning web application for credit card approval prediction using Extra Trees Classifier, achieving exceptional performance with an AUC Score of 0.8878. This project went beyond the competition requirements of submitting a video demo, proposal, and model notebook to deliver a fully functional website demonstrating real-world stakeholder benefits.

## 🎯 Project Overview

This project was developed for the **Data Science ICONIC IT Competition**, where our team achieved **first place**. Beyond meeting the competition requirements (video demo, proposal, and model notebook), we created a comprehensive web application that showcases the practical benefits of our machine learning solution for real stakeholders.

### Competition Achievement
- 🥇 **First Place Winner** - Data Science ICONIC IT Competition
- 🚀 **Beyond Requirements** - Built full-stack web application exceeding competition scope
- 💼 **Stakeholder Focus** - Demonstrated real-world business value

### Project Objectives
- **Process Automation**: Accelerate credit card approval processes through ML automation
- **Risk Reduction**: Minimize credit default risk with accurate predictive modeling
- **Operational Efficiency**: Streamline credit application assessment workflows
- **User Experience**: Provide instant, reliable feedback to credit applicants

## 🌐 Website Development

### Technology Stack
- **Frontend**: HTML, CSS (Bootstrap), JavaScript for responsive and interactive user interface
- **Backend**: Flask framework for robust server-side logic and ML model integration
- **Deployment**: Hosted on OnRender for reliable online accessibility
- **Machine Learning**: Python-based model integration with real-time prediction capabilities

### Key Features
- **Interactive Forms**: User-friendly data input with real-time validation
- **Real-time Predictions**: Instant classification results upon form submission
- **Visual Feedback**: Clear visualization of model predictions for stakeholder decision-making
- **Responsive Design**: Mobile-friendly interface ensuring accessibility across devices
- **Error Handling**: Comprehensive validation and user feedback systems

## 🏗️ Project Architecture

```
creditcard-approval-classification-website/
├── 📄 app.py                          # Flask application
├── 🤖 et_model.pkl                    # Trained Extra Trees model
├── 📊 feature_names.json              # Feature configuration
├── 📋 requirements.txt                # Python dependencies
├── 📁 static/
│   └── assets/                        # Images, logos, styling assets
├── 📁 templates/
│   ├── landingpage.html              # Homepage
│   ├── model.html                    # Prediction interface
│   └── aboutus.html                  # Team information
└── 📁 Notebook Modeling/
    ├── HaloRek.ipynb                 # Model development notebook
    └── BACA SAYA.txt                 # Development notes
```

## 🧠 Machine Learning Implementation

### Model Development Process
Our **Extra Trees Classifier** was selected for its superior robustness and ability to reduce overfitting, achieving an impressive **AUC score of 0.8878** - ideal for handling imbalanced datasets.

#### Key Development Steps:

**1. Data Preparation**
- **Missing Value Imputation**: 
  - Numerical features: Median imputation
  - Categorical features: Mode imputation

**2. Feature Engineering**
- **Correlation Analysis**: Removed redundant numerical features with high correlation
- **Variance Inflation Factor (VIF)**: Eliminated multicollinear features
- **Hypothesis Testing**: Applied Chi-Square tests to exclude statistically insignificant categorical features (e.g., "Car_Owner")

**3. Model Evaluation & Selection**
- **Algorithm Comparison**: Tested multiple classifiers (Random Forest, XGBoost, Extra Trees)
- **Performance Metric**: Selected Extra Trees Classifier for superior AUC score of 0.8878
- **Validation**: Cross-validation to ensure robust performance on unseen data

### Model Performance
| Metric | Score |
|--------|-------|
| **AUC Score** | 0.8878 |
| **Algorithm** | Extra Trees Classifier |
| **Features** | 15 optimized features |
| **Preprocessing** | Imputation + Feature Selection + Hypothesis Testing |

### Model Features
1. **Annual Income** - Annual income
2. **Education Level** - Education level
3. **Income Type** - Income type
4. **Housing Type** - Housing type
5. **Family Members** - Number of family members
6. **Age** - Applicant age
7. **Employment Years** - Years of employment
8. **Income per Person** - Income per person
9. **Car Ownership** - Car ownership
10. **Property Ownership** - Property ownership
11. **Work Phone** - Work phone number
12. **Email** - Email address
13. **Family Status** - Family status
14. **Occupation Type** - Occupation type
15. **Gender** - Gender

## 🛠️ Setup & Installation

### Prerequisites
- **Python 3.7+**
- **Flask** for web framework
- **scikit-learn** for machine learning
- **pandas & numpy** for data processing

### Quick Start

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd creditcard-approval-classification-website
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application:**
   ```bash
   python app.py
   ```

4. **Access application:**
   ```
   http://localhost:5000
   ```

## 💻 Usage

### Web Interface

1. **Landing Page** (`/`): 
   - Information about HaloRek
   - AI model explanation
   - Navigation to prediction tool

2. **Model Prediction** (`/model`):
   - Input form with 15 features
   - Real-time validation
   - Instant prediction results
   - Retry functionality

3. **About Us** (`/aboutus`):
   - HaloRek team profiles
   - Logo philosophy
   - Project background

### Prediction Flow

```python
# Example prediction workflow
1. User fills prediction form
2. Data validation (client & server side)
3. Feature preprocessing
4. Model inference with et_model.pkl
5. Result display (APPROVED/REJECTED)
6. Option to retry with new data
```

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#002D62` - Trust & professionalism
- **Accent Yellow**: `#E6DE01` - Energy & optimism  
- **Light Gray**: `#F6F9FF` - Clean & modern
- **Text Gray**: `#3E4756` - Readability

### Typography
- **Primary Font**: Open Sans (web-safe, readable)
- **Accent Font**: Inter (modern, clean)

### UI Components
- **Bootstrap 5.3.3** for responsive grid
- **Custom CSS** for brand consistency
- **Font Awesome** for icons
- **Interactive animations** for better UX

## 💼 My Contributions (Team Leader)

As the **Team Leader** of HaloRek, I spearheaded multiple critical aspects of this competition-winning project:

### Leadership & Coordination
- **Team Management**: Led and coordinated all team activities and task distribution
- **Project Planning**: Established project timeline and milestone tracking
- **Communication**: Facilitated team collaboration and maintained project momentum

### Machine Learning Development
- **Model Architecture**: Designed and implemented the Extra Trees Classifier
- **Data Preprocessing**: Developed comprehensive data cleaning and imputation strategies
- **Feature Engineering**: Conducted correlation analysis, VIF calculation, and Chi-Square testing
- **Model Evaluation**: Implemented cross-validation and performance optimization

### Full-Stack Development
- **Frontend Development**: Designed responsive user interface using HTML, CSS, and Bootstrap
- **Backend Development**: Built Flask application with robust server-side logic
- **Model Integration**: Seamlessly integrated ML model into web application
- **Deployment**: Managed deployment process on OnRender platform

### Technical Innovation
- **Beyond Competition Scope**: Extended project from required deliverables to full web application
- **Stakeholder Value**: Focused on demonstrating real-world business benefits
- **User Experience**: Prioritized intuitive design for practical usability

## 👥 Team HaloRek

| Name | Study Program | Class | Role |
|------|---------------|-------|------|
| **Dwi Anggara Najwan Sugama** | Software Engineering Technology | 2023 | **Team Leader**, ML Engineer & Full-stack Developer |
| **Muhammad Natha Ulinnuha** | Computer Science | 2023 | Data Scientist |
| **Naufal Afif Bauw** | Computer Science | 2023 | UI/UX Designer |

## 🔬 Technical Deep Dive

### Advanced Feature Engineering Process

**1. Data Exploration & Quality Assessment**
- Comprehensive analysis of credit card application dataset
- Missing data pattern identification and handling strategy
- Feature distribution analysis and outlier detection

**2. Statistical Feature Selection**
- **Correlation Analysis**: Identified and removed highly correlated numerical features
- **Variance Inflation Factor (VIF)**: Eliminated multicollinear features to prevent model overfitting
- **Chi-Square Testing**: Applied hypothesis testing to categorical features
  - Removed statistically insignificant features (e.g., "Car_Owner" with p-value > 0.05)
- **Feature Importance Ranking**: Evaluated feature contributions using statistical methods

**3. Model Selection Methodology**
- **Algorithm Comparison**: Systematically evaluated Random Forest, XGBoost, and Extra Trees
- **Cross-Validation**: 5-fold stratified cross-validation for robust performance estimation
- **Hyperparameter Optimization**: Grid search for optimal model configuration
- **Imbalanced Data Handling**: Selected Extra Trees for superior performance on imbalanced datasets

**4. Production Model Pipeline**
```python
# Model training and evaluation pipeline
1. Data Preprocessing (imputation, encoding)
2. Feature Engineering (correlation, VIF, Chi-Square)
3. Model Training (Extra Trees with optimized parameters)
4. Validation (cross-validation, AUC evaluation)
5. Model Persistence (pickle serialization for deployment)
```

### Production Deployment

```python
# Model loading and prediction
import pickle
import pandas as pd

# Load trained model
with open('et_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Make prediction
def predict_approval(features):
    prediction = model.predict_proba([features])
    return prediction[0][1]  # Probability of approval
```

## 🚀 Future Enhancements

- [ ] **Real-time Model Updates**: Automatic retraining pipeline
- [ ] **Advanced Analytics**: Detailed prediction explanations
- [ ] **API Integration**: RESTful API for external systems
- [ ] **Mobile App**: Native mobile application
- [ ] **Database Integration**: User history & analytics storage
- [ ] **A/B Testing**: Model performance comparison
- [ ] **Security Features**: Enhanced data protection

### Web Development
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Guide](https://getbootstrap.com/docs/5.3/)

## 📞 Support & Contact

For questions or technical support, please contact the HaloRek team through repository issues or contact information available in the application.

---

## 🏆 Competition Success & Recognition

**Data Science ICONIC IT Competition - First Place Winner**

This project demonstrates our ability to:
- Exceed competition requirements by delivering a complete web application
- Apply advanced machine learning techniques for real-world business problems
- Lead cross-functional teams to achieve outstanding results
- Bridge the gap between academic research and practical implementation

*Developed with ❤️ by Team HaloRek - Revolutionizing credit approval with AI*

---

**Project Leader**: Dwi Anggara Najwan Sugama  
**Competition**: Data Science ICONIC IT Competition 2024  
**Achievement**: 🥇 First Place Winner  
**Technology Stack**: Python, Flask, scikit-learn, Bootstrap, OnRender

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
