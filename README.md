# 🏥 Health Insurance Charges Prediction API 💸

A **Flask-based REST API** to train, test, and predict health insurance charges using a **Linear Regression model**.  
Easily train your model, evaluate performance, and predict insurance charges with simple API calls.  

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🏋️ Train | Upload a CSV file to train the model |
| 📊 Test | Upload a CSV file to evaluate model (R², MSE, MAE) |
| 💰 Predict | Get predicted insurance charges for a single input |

---

## 🛠️ API Endpoints

### 1️⃣ `/train` (POST)
- **Description:** Train the Linear Regression model  
- **CSV Columns:** `age, sex, bmi, children, smoker, region, charges`  

**Postman Request:**

