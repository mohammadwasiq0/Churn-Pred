import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

def load_data(file_path):
    """Load the dataset."""
    return pd.read_csv(file_path)

def preprocess_data(df, is_training=True):
    """
    Preprocess the data. If training, fit the scalers/encoders.
    If predicting, use the saved scalers/encoders.
    """
    df_processed = df.copy()
    
    # Drop Customer ID
    if 'customerID' in df_processed.columns:
        df_processed = df_processed.drop('customerID', axis=1)
        
    # Handle TotalCharges if it's object (it might have blanks)
    if df_processed['TotalCharges'].dtype == 'object':
        df_processed['TotalCharges'] = pd.to_numeric(df_processed['TotalCharges'].replace(' ', np.nan))
        df_processed['TotalCharges'].fillna(0, inplace=True)
        
    categorical_cols = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 
        'PaperlessBilling', 'PaymentMethod'
    ]
    
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../models')
    os.makedirs(models_dir, exist_ok=True)
    
    if is_training:
        # Encode target if present
        if 'Churn' in df_processed.columns:
            df_processed['Churn'] = df_processed['Churn'].map({'Yes': 1, 'No': 0})
            
        # Label Encoding for categorical columns
        encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col])
            encoders[col] = le
            
        # Save encoders
        joblib.dump(encoders, os.path.join(models_dir, 'label_encoders.pkl'))
        
        # Scale numerical columns
        scaler = StandardScaler()
        df_processed[numerical_cols] = scaler.fit_transform(df_processed[numerical_cols])
        
        # Save scaler
        joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
        
    else:
        # Load encoders & scaler
        try:
            encoders = joblib.load(os.path.join(models_dir, 'label_encoders.pkl'))
            scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
            
            # Apply encoders (handling unknown labels gracefully)
            for col in categorical_cols:
                le = encoders[col]
                # If new category appears in production, map to most frequent or 0
                df_processed[col] = df_processed[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else 0
                )
                
            # Apply scaler
            df_processed[numerical_cols] = scaler.transform(df_processed[numerical_cols])
                
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
            
    return df_processed

if __name__ == "__main__":
    # Test preprocessing
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/churn_dataset.csv')
    df = load_data(data_path)
    processed_df = preprocess_data(df, is_training=True)
    print("Data preprocessed successfully. Shape:", processed_df.shape)
