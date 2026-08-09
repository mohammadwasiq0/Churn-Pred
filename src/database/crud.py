from sqlalchemy.orm import Session
from src.database.models import PredictionLog

def log_prediction(db: Session, features: dict, prediction_result: dict, drift_score: float = None, is_anomaly: bool = False):
    """
    Log a new prediction and its inputs to the database.
    """
    db_log = PredictionLog(
        features=features,
        prediction=prediction_result['prediction'],
        probability=prediction_result['probability'],
        churn_risk=prediction_result['churn_risk'],
        drift_score=drift_score,
        is_anomaly=1 if is_anomaly else 0
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_recent_logs(db: Session, limit: int = 100):
    """
    Retrieve recent predictions for dashboard monitoring.
    """
    return db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(limit).all()

def get_aggregate_stats(db: Session):
    """
    Get aggregated statistics for dashboard.
    """
    total_predictions = db.query(PredictionLog).count()
    high_risk = db.query(PredictionLog).filter(PredictionLog.churn_risk == 'High').count()
    medium_risk = db.query(PredictionLog).filter(PredictionLog.churn_risk == 'Medium').count()
    low_risk = db.query(PredictionLog).filter(PredictionLog.churn_risk == 'Low').count()
    overall_anomalies = db.query(PredictionLog).filter(PredictionLog.is_anomaly == 1).count()
    
    return {
        "total_predictions": total_predictions,
        "high_risk_predictions": high_risk,
        "medium_risk_predictions": medium_risk,
        "low_risk_predictions": low_risk,
        "anomalies_detected": overall_anomalies,
        "high_risk_percentage": (high_risk / total_predictions * 100) if total_predictions > 0 else 0
    }
