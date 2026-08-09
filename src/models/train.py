import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.preprocessing import preprocess_data

def train_model():
    """
    Train a Random Forest model with MLflow tracking.
    """
    # Load and preprocess data
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/churn_dataset.csv')
    df = pd.read_csv(data_path)
    
    # Preprocess (fit encoders and scalers)
    df_processed = preprocess_data(df, is_training=True)
    
    # Split features and target
    target_col = 'Churn'
    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    import pathlib
    mlflow_dir = pathlib.Path(__file__).parent.parent.parent / "mlruns"
    os.makedirs(mlflow_dir, exist_ok=True)
    mlflow.set_tracking_uri(mlflow_dir.resolve().as_uri())
    mlflow.set_experiment('churn_prediction')
    
    with mlflow.start_run():
        # Hyperparameters
        n_estimators = 100
        max_depth = 10
        random_state = 42
        
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators, 
            max_depth=max_depth, 
            random_state=random_state,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        print(f"Accuracy: {acc:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"ROC AUC: {roc_auc:.4f}")
        
        # Log metrics
        mlflow.log_metrics({
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "roc_auc": roc_auc
        })
        
        # Log model
        mlflow.sklearn.log_model(model, "random_forest_model")
        
        # Save model locally for fast inference
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../models')
        os.makedirs(models_dir, exist_ok=True)
        model_path = os.path.join(models_dir, 'churn_model.pkl')
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Training complete.")
