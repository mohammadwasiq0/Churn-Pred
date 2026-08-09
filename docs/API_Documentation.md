# API Documentation

The Churn Prediction Platform exposes a set of RESTful endpoints via FastAPI. 

## Base URL
When running locally, the API is available at: `http://127.0.0.1:8000`

---

## 🔮 Predictions Endpoints

### 1. **Single Prediction**
Use this endpoint to predict the churn risk of a single customer by submitting their features in JSON format.

- **URL:** `/predict/`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Body (JSON):**
```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "Yes",
  "StreamingTV": "Yes",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 50.0,
  "TotalCharges": 600.0
}
```

**Response (JSON):**
```json
{
  "prediction": 1,
  "probability": 0.724,
  "churn_risk": "High",
  "drift_score": 0.0,
  "is_anomaly": false,
  "anomalies": []
}
```

---

### 2. **Batch Prediction (Bulk CSV)**
Upload a CSV containing multiple rows of customer features to predict their churn probabilities in bulk.

- **URL:** `/predict/batch`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`

**Form Data Parameters:**
- `file`: The `.csv` file upload containing the exact column names as expected by the model.

**Response:**
Returns a continuously downloadable stream formatted as `"text/csv"`. The result file includes all the original features plus the newly appended tracking columns: `Prediction`, `Probability`, `Churn_Risk`, `Drift_Score`, and `Is_Anomaly`.

---

## 📊 Dashboard & Monitoring Endpoints

### 3. **Fetch Telemetry Analytics**
Returns live aggregated metrics measuring prediction distributions.

- **URL:** `/dashboard/stats`
- **Method:** `GET`

**Response (JSON):**
```json
{
  "total_predictions": 542,
  "high_risk_predictions": 123,
  "medium_risk_predictions": 204,
  "low_risk_predictions": 215,
  "anomalies_detected": 4,
  "high_risk_percentage": 22.69
}
```

---

### 4. **Fetch Recent Logs**
Used to populate the Live Monitoring telemetry table indexing the most recent guardrail flags and drift bounds.

- **URL:** `/dashboard/recent-logs?limit=15`
- **Method:** `GET`

**Response (JSON Array):**
```json
[
  {
    "id": 542,
    "timestamp": "2026-03-07T21:20:01.324Z",
    "prediction": 1,
    "probability": 0.88,
    "churn_risk": "High",
    "drift_score": 0.0,
    "is_anomaly": false,
    "features": { "gender": "Male", "MonthlyCharges": 95.5, "..." : "..." }
  }
]
```

---

### 5. **Fetch MLflow Metrics**
Retrieves the most recent Random Forest model performance stats from MLflow's registry natively tracing data without SQL persistence.

- **URL:** `/dashboard/mlflow-metrics`
- **Method:** `GET`

**Response (JSON):**
```json
{
  "metrics": {
    "accuracy": 0.686,
    "precision": 0.5075,
    "recall": 0.3218,
    "f1": 0.3938,
    "roc_auc": 0.6674
  },
  "params": {
    "max_depth": "10",
    "n_estimators": "100"
  }
}
```
