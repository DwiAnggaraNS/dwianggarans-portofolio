## Credit Card Approval Classification Website (HaloRek)

Production-style Flask app for real-time credit card approval prediction using an Extra Trees Classifier. Built by Team HaloRek (competition winner) and packaged as a simple web app with a JSON prediction API.

### Key Features
- Extra Trees model served with Flask
- Clean HTML templates for landing, model form, and about pages
- JSON prediction endpoint with input validation
- Deterministic preprocessing aligned to training features from `feature_names.json`

## Project Structure

```
creditcard-approval-classification-website/
├── app.py                   # Flask app (routes + inference)
├── et_model.pkl             # Trained Extra Trees model (pickle)
├── feature_names.json       # Ordered feature list expected by the model
├── requirements.txt         # Python dependencies
├── static/                  # Assets (images, css)
└── templates/               # Jinja2 templates (landingpage, model, aboutus)
```

## Requirements
- Python 3.8+
- Packages from `requirements.txt` (Flask, pandas, scikit-learn)

## Quick Start
1) Create and activate a virtual environment (Windows PowerShell):
```
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Run the app:
```
python app.py
```
4) Open http://localhost:5000

## Routes
- GET `/` → landing page
- GET `/model` → prediction form UI
- GET `/aboutus` → team/profile page
- POST `/predict` → JSON prediction API

## Prediction API
Endpoint: `POST /predict`

Content-Type: `application/json`

Request body fields (required):
- Annual_income: number (float)
- Employed_days: number (int)
- Family_Members: number (int)
- Birthday_count: number (int; if positive, the server will convert it to negative days)
- Type_Income: string
- Housing_type: string
- Type_Occupation: string
- EDUCATION: string

Notes:
- The server constructs a pandas DataFrame with columns from `feature_names.json`, initializes to 0, then fills your provided fields.
- Feature names must match exactly with the keys above (case-sensitive as shown).

Example request:
```
POST /predict
Content-Type: application/json

{
   "Annual_income": 65000000,
   "Employed_days": 1200,
   "Family_Members": 3,
   "Birthday_count": 9000,
   "Type_Income": "Working",
   "Housing_type": "House / apartment",
   "Type_Occupation": "Laborers",
   "EDUCATION": "Secondary / secondary special"
}
```

Response:
```
{ "prediction": "Approved" }  # or "Rejected"
```

## Troubleshooting
- Ensure `et_model.pkl` and `feature_names.json` sit next to `app.py`.
- If you update training features, regenerate `feature_names.json` and the model together.
- For pandas or scikit-learn version issues, use the exact versions in `requirements.txt`.

## License
MIT (add a LICENSE file if you plan to distribute)
