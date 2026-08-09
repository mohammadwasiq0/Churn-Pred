# Low-Level Design (LLD)
## Component Specifications

### 1. `src/data/preprocessing.py`
This module handles feature normalization, scaling, and categorical encoding.

- **`load_data(file_path: str)`**: Reads the `.csv` dataset yielding a pandas DataFrame.
- **`preprocess_data(df: DataFrame, is_training: bool)`**: 
  - If `is_training=True`: Generates StandardScalers and LabelEncoders, mapping features systematically. Writes transformations binaries out to `models/label_encoders.pkl` and `models/scaler.pkl` respectively using `joblib`.
  - If `is_training=False`: Extracts and loads previously fitted transform pipelines globally masking unknowns safely to index `0` or raising gracefully.

### 2. `src/models/train.py`
Connects the data transformations natively to algorithmic MLflow pipelines.

- **`train_model()`**: Orchestrates full data load explicitly pointing at locally initialized `mlruns/` directories.
  - Generates an optimal `RandomForestClassifier` configuration balancing class biases properly using `class_weight='balanced'`.
  - Commits artifacts accurately tracing Accuracy, Recall, Precision, and ROC_AUC into MLflow storage formats.
  - Drops finalized binary to globally accessible paths.

### 3. `src/models/predict.py`
Implements the Singleton `ChurnPredictor` logic minimizing memory overhead in concurrent FastAPI loads.

- **`ChurnPredictor` Class Definition**:
  - `load_model()`: Validates path and initiates static instance tracking dynamically via local fields.
  - `predict(input_data: dict)`: Pushes feature parameters via pandas logic directly into `preprocess_data`, resolving binary payload evaluations systematically. Transforms numerical probability limits systematically yielding High/Medium/Low markers effectively.

### 4. `src/monitoring/guardrails.py`
Defines bounds maps explicitly indexing acceptable ranges globally.

- **`Guardrails` Class Definition**:
  - Contains bounded map dict definitions corresponding explicitly to numeric features `['tenure', 'MonthlyCharges', 'TotalCharges']` and categoricals.
  - `check_inputs()`: Scans dictionaries actively counting anomalous mismatches. Calculates internal drift index. Raises flags recursively dynamically.

### 5. `api/schemas.py`
Constructs explicit `BaseModels` relying heavily on strictly defined Pydantic field validators indexing integers, strings, floats tightly.

```python
class PredictionResponse(BaseModel):
    prediction: int    # 1 or 0
    probability: float # Score from 0 to 1
    churn_risk: str    # High, Medium, Low
    drift_score: float # Guardrail result
    is_anomaly: bool   # Guardrail result
```

### 6. `api/routes/predictions.py` and `dashboard.py`

- Handles API requests via dependency-injected SQLAlchemy active sessions.
- Traces `log_prediction` globally parsing dictionary inputs correctly recursively inserting metrics actively inside SQLite schemas natively tracing telemetry globally.
- Triggers active endpoints tracing MLFlow payloads utilizing the python bindings cleanly pulling runs indexing directly. 

### 7. Global SQLite Models
- **`PredictionLog`**: Base declarative indexing mapping out schema configurations accurately tracking input maps via `JSON` types efficiently scaling database footprint safely natively. 
