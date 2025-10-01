from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

MODEL_PATH = "model.pkl"

# Helper: preprocess dataset
def preprocess(df):
    encoders = {}
    for col in ['sex', 'smoker', 'region']:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
    return df, encoders

@app.route("/train", methods=["POST"])
def train():
    if "file" not in request.files:
        return jsonify({"error": "CSV file required"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    if "charges" not in df.columns:
        return jsonify({"error": "CSV must have 'charges' column"}), 400

    df, encoders = preprocess(df)
    X = df.drop(columns=["charges"])
    y = df["charges"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model and encoders
    joblib.dump({"model": model, "encoders": encoders, "features": list(X.columns)}, MODEL_PATH)

    return jsonify({"status": "ok", "message": "Model trained successfully"}), 200

@app.route("/test", methods=["POST"])
def test():
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Train the model first"}), 400
    if "file" not in request.files:
        return jsonify({"error": "CSV file required"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    df, _ = preprocess(df)
    X = df.drop(columns=["charges"])
    y = df["charges"]

    obj = joblib.load(MODEL_PATH)
    model = obj["model"]

    preds = model.predict(X)
    mse = mean_squared_error(y, preds)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)

    return jsonify({"mse": mse, "mae": mae, "r2": r2}), 200

@app.route("/predict", methods=["POST"])
def predict():
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "Train the model first"}), 400

    data = request.get_json()
    obj = joblib.load(MODEL_PATH)
    model = obj["model"]
    encoders = obj["encoders"]
    features = obj["features"]

    df = pd.DataFrame([data])

    for col, le in encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col])

    df = df[features]

    pred = model.predict(df)[0]

    return jsonify({"predicted_charges": float(pred)}), 200

if __name__ == "__main__":
    app.run(debug=True)
