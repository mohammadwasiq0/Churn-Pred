import joblib
import os
import pandas as pd
from src.data.preprocessing import preprocess_data

class ChurnPredictor:
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../models')
        self.model_path = os.path.join(self.models_dir, 'churn_model.pkl')
        self.model = None

    def load_model(self):
        """Lazy load the model when needed."""
        if self.model is None:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}. Run train.py first.")
            self.model = joblib.load(self.model_path)
            
    def predict(self, input_data: dict):
        """
        Make probability prediction for churn.
        """
        self.load_model()
        
        # Convert to DataFrame
        df = pd.DataFrame([input_data])
        
        # Preprocess using saved scalers and encoders
        df_processed = preprocess_data(df, is_training=False)
        
        # Make prediction
        prediction = self.model.predict(df_processed)[0]
        probability = self.model.predict_proba(df_processed)[0][1]
        
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "churn_risk": "High" if probability > 0.6 else "Medium" if probability > 0.3 else "Low"
        }

if __name__ == "__main__":
    predictor = ChurnPredictor()
    sample = {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'No',
        'tenure': 1,
        'PhoneService': 'No',
        'MultipleLines': 'No phone service',
        'InternetService': 'DSL',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 29.85,
        'TotalCharges': 29.85
    }
    print(predictor.predict(sample))
