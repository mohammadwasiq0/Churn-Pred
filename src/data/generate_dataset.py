import pandas as pd
import numpy as np
import os

def generate_churn_data(num_records=5000, seed=42):
    """
    Generate synthetic data for telecom churn prediction.
    """
    np.random.seed(seed)
    
    # Generate customer IDs
    customer_ids = [f'CUST_{str(i).zfill(5)}' for i in range(1, num_records + 1)]
    
    # Demographics
    gender = np.random.choice(['Male', 'Female'], num_records)
    senior_citizen = np.random.choice([0, 1], num_records, p=[0.85, 0.15])
    partner = np.random.choice(['Yes', 'No'], num_records)
    dependents = np.random.choice(['Yes', 'No'], num_records)
    
    # Service details
    tenure = np.random.randint(1, 73, num_records) # 1 to 72 months
    phone_service = np.random.choice(['Yes', 'No'], num_records, p=[0.9, 0.1])
    multiple_lines = np.where(phone_service == 'Yes', 
                             np.random.choice(['Yes', 'No', 'No phone service'], num_records), 
                             'No phone service')
    
    internet_service = np.random.choice(['DSL', 'Fiber optic', 'No'], num_records, p=[0.4, 0.4, 0.2])
    
    online_security = np.where(internet_service != 'No', 
                              np.random.choice(['Yes', 'No'], num_records), 
                              'No internet service')
    online_backup = np.where(internet_service != 'No', 
                            np.random.choice(['Yes', 'No'], num_records), 
                            'No internet service')
    device_protection = np.where(internet_service != 'No', 
                                np.random.choice(['Yes', 'No'], num_records), 
                                'No internet service')
    tech_support = np.where(internet_service != 'No', 
                           np.random.choice(['Yes', 'No'], num_records), 
                           'No internet service')
    streaming_tv = np.where(internet_service != 'No', 
                           np.random.choice(['Yes', 'No'], num_records), 
                           'No internet service')
    streaming_movies = np.where(internet_service != 'No', 
                               np.random.choice(['Yes', 'No'], num_records), 
                               'No internet service')
    
    # Account details
    contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], num_records, p=[0.5, 0.25, 0.25])
    paperless_billing = np.random.choice(['Yes', 'No'], num_records)
    payment_method = np.random.choice([
        'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'
    ], num_records)
    
    # Charges
    monthly_charges = np.random.uniform(18.0, 120.0, num_records)
    total_charges = monthly_charges * tenure + np.random.uniform(0, 50, num_records) # Add some noise
    
    # Target Variable: Churn
    # We create rules to make it somewhat realistic
    churn_prob = np.zeros(num_records)
    
    # Month-to-month contracts churn more
    churn_prob += np.where(contract == 'Month-to-month', 0.2, 0)
    
    # Fiber optic churn slightly more if no tech support
    churn_prob += np.where((internet_service == 'Fiber optic') & (tech_support == 'No'), 0.15, 0)
    
    # High monthly charges increase churn
    churn_prob += np.where(monthly_charges > 80, 0.1, 0)
    
    # Low tenure increases churn
    churn_prob += np.where(tenure < 12, 0.1, 0)
    
    # Base probability + noise
    churn_prob += np.random.uniform(0.05, 0.15, num_records)
    
    # Normalize and convert to binary
    churn_prob = np.clip(churn_prob, 0, 1)
    churn = (np.random.rand(num_records) < churn_prob).astype(int)
    churn_labels = np.where(churn == 1, 'Yes', 'No')
    
    # Create DataFrame
    data = {
        'customerID': customer_ids,
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': np.round(monthly_charges, 2),
        'TotalCharges': np.round(total_charges, 2),
        'Churn': churn_labels
    }
    
    df = pd.DataFrame(data)
    
    # Save the dataset
    os.makedirs('../../data', exist_ok=True)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/churn_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} records and saved to {output_path}")
    
    return df

if __name__ == "__main__":
    generate_churn_data()
