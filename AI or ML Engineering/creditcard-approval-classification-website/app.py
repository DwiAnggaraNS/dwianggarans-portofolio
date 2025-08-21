from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import json

app = Flask(__name__)

# Load the model
with open('et_model.pkl', 'rb') as file:
    model_classifier = pickle.load(file)

# Load feature names
with open('feature_names.json', 'r') as f:
    feature_names = json.load(f)

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method != 'POST':
        return jsonify({'error': 'Only POST requests are allowed'}), 405
    
    data = request.json
    
    # Create a DataFrame with all features initialized to 0
    input_df = pd.DataFrame(0, index=[0], columns=feature_names)

    # Check Birthday_Count format. If it's positive, then convert into negative format
    data['Birthday_count'] = int(data['Birthday_count'])
    if data['Birthday_count'] > 0:
        data['Birthday_count'] *= -1
    else:
        pass

    # Fill in the numeric features
    input_df['Annual_income'] = float(data['Annual_income'])
    input_df['Employed_days'] = int(data['Employed_days'])
    input_df['Family_Members'] = int(data['Family_Members'])
    input_df['Birthday_count'] = float(data['Birthday_count'])
    input_df['Type_Income'] = str(data['Type_Income'])
    input_df['Housing_type'] = str(data['Housing_type'])
    input_df['Type_Occupation'] = str(data['Type_Occupation'])
    input_df['EDUCATION'] = str(data['EDUCATION'])
    
    # Make prediction
    prediction = model_classifier.predict(input_df)[0]  # This will return 0 or 1
    
    result = "Approved" if prediction == 1 else "Rejected"
    
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)