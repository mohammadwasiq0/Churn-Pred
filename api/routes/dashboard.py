from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.models import SessionLocal
from src.database.crud import get_recent_logs, get_aggregate_stats
import mlflow
import os
import pathlib

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def fetch_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get aggregate metrics.
    """
    return get_aggregate_stats(db)

@router.get("/recent-logs", response_model=list[dict])
def fetch_recent_logs(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get latest predictions and guardrail outputs.
    """
    logs = get_recent_logs(db, limit=limit)
    response = []
    
    for row in logs:
        log_entry = {
            "id": row.id,
            "timestamp": row.timestamp.isoformat(),
            "prediction": row.prediction,
            "probability": row.probability,
            "churn_risk": row.churn_risk,
            "drift_score": row.drift_score,
            "is_anomaly": bool(row.is_anomaly),
            "features": row.features
        }
        response.append(log_entry)
        
    return response

@router.get("/mlflow-metrics")
def fetch_mlflow_metrics():
    """
    Get latest MLflow model metrics.
    """
    try:
        mlflow_dir = pathlib.Path(__file__).parent.parent.parent / "mlruns"
        mlflow.set_tracking_uri(mlflow_dir.resolve().as_uri())
        runs = mlflow.search_runs(experiment_names=["churn_prediction"])
        if len(runs) > 0:
            latest_run = runs.iloc[0]
            # Extract metrics (columns starting with 'metrics.')
            metrics = {col.replace('metrics.', ''): latest_run[col] for col in latest_run.index if col.startswith('metrics.')}
            # Add parameters like max_depth, n_estimators if requested
            params = {col.replace('params.', ''): latest_run[col] for col in latest_run.index if col.startswith('params.')}
            return {"metrics": metrics, "params": params}
        return {"metrics": {}, "params": {}}
    except Exception as e:
        return {"error": str(e)}
