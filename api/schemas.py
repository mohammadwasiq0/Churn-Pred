from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    gender: str = Field(..., description="Customer gender (Male/Female)")
    SeniorCitizen: int = Field(..., description="Is the customer a senior citizen (1/0)")
    Partner: str = Field(..., description="Has a partner (Yes/No)")
    Dependents: str = Field(..., description="Has dependents (Yes/No)")
    tenure: int = Field(..., description="Tenure in months", ge=0)
    PhoneService: str = Field(..., description="Has phone service (Yes/No)")
    MultipleLines: str = Field(..., description="Has multiple lines (Yes/No/No phone service)")
    InternetService: str = Field(..., description="Internet service type (DSL/Fiber optic/No)")
    OnlineSecurity: str = Field(..., description="Online security service (Yes/No/No internet service)")
    OnlineBackup: str = Field(..., description="Online backup service (Yes/No/No internet service)")
    DeviceProtection: str = Field(..., description="Device protection service (Yes/No/No internet service)")
    TechSupport: str = Field(..., description="Tech support service (Yes/No/No internet service)")
    StreamingTV: str = Field(..., description="Streaming TV service (Yes/No/No internet service)")
    StreamingMovies: str = Field(..., description="Streaming movies service (Yes/No/No internet service)")
    Contract: str = Field(..., description="Contract type (Month-to-month/One year/Two year)")
    PaperlessBilling: str = Field(..., description="Uses paperless billing (Yes/No)")
    PaymentMethod: str = Field(..., description="Payment method used")
    MonthlyCharges: float = Field(..., description="Monthly charge amount")
    TotalCharges: float = Field(..., description="Total amount charged")

class PredictionResponse(BaseModel):
    prediction: int    # 1 or 0
    probability: float # Score from 0 to 1
    churn_risk: str    # High, Medium, Low
    drift_score: float # Guardrail result
    is_anomaly: bool   # Guardrail result
    anomalies: list[str] = [] # Messages about drifted inputs
