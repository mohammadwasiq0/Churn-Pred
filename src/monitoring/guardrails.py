import numpy as np

class Guardrails:
    """
    Implements production-grade checks for ML inputs.
    Validates data quality, bounds, and performs basic outlier detection.
    """
    def __init__(self):
        # Expected ranges based on training data
        self.bounds = {
            'tenure': (0, 75),
            'MonthlyCharges': (10.0, 150.0),
            'TotalCharges': (0.0, 10000.0)
        }
        
        self.categories = {
            'gender': ['Male', 'Female'],
            'Partner': ['Yes', 'No'],
            'Dependents': ['Yes', 'No'],
            'PhoneService': ['Yes', 'No'],
            'InternetService': ['DSL', 'Fiber optic', 'No'],
            'Contract': ['Month-to-month', 'One year', 'Two year']
        }

    def check_inputs(self, input_data: dict):
        """
        Validate input data against expected bounds and categories.
        Returns a drift score (0.0 = perfect, higher = anomalous) and is_anomaly flag.
        """
        anomalies = []
        drift_score = 0.0
        
        # Check numerical bounds
        for num_feat, (min_val, max_val) in self.bounds.items():
            if num_feat in input_data:
                val = float(input_data[num_feat])
                if val < min_val or val > max_val:
                    anomalies.append(f"{num_feat} out of bounds: {val}")
                    drift_score += 1.0 # Significant drift
                    
        # Check categorical valid values
        for cat_feat, valid_cats in self.categories.items():
            if cat_feat in input_data:
                if input_data[cat_feat] not in valid_cats:
                    anomalies.append(f"Unexpected category for {cat_feat}: {input_data[cat_feat]}")
                    drift_score += 0.5 # Moderate drift
                    
        is_anomaly = drift_score > 0.0
        
        return {
            "drift_score": drift_score,
            "is_anomaly": is_anomaly,
            "anomalies": anomalies
        }

guardrails = Guardrails()
