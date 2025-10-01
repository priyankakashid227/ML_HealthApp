# Health Insurance Charges Prediction API

Flask-based ML API to train, test, and predict medical insurance charges.

s## Endpoints

### 1. /train (POST)
- Input: CSV file (form-data, key=`file`)
- Output: 
{
  "status": "ok",
  "message": "Model trained successfully"
}

### 2. /test (POST)
- Input: CSV file (form-data, key=`file`)
- Output example:
{
  "mse": 123456.78,
  "mae": 987.65,
  "r2": 0.85
}

### 3. /predict (POST)
- Input: JSON (one row from CSV, without `charges`)
- Example:
{
  "age": 30,
  "sex": "female",
  "bmi": 28.5,
  "children": 1,
  "smoker": "no",
  "region": "southeast"
}
- Output example:
{
  "predicted_charges": 12045.67
}

## How to Run

1. Install dependencies:
# ML_HealthApp
Flask ML API for Health Insurance Charges Prediction
