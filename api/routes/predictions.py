from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
import pandas as pd
import io
from sqlalchemy.orm import Session
from api.schemas import PredictionInput, PredictionResponse
from src.models.predict import ChurnPredictor
from src.monitoring.guardrails import guardrails
from src.database.models import SessionLocal
from src.database.crud import log_prediction

router = APIRouter(prefix="/predict", tags=["Predictions"])

# Singleton Predictor
predictor = ChurnPredictor()

# Dependency pipeline for SQLite DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PredictionResponse)
def make_prediction(request: PredictionInput, db: Session = Depends(get_db)):
    """
    Make a churn prediction based on customer features.
    """
    input_data = request.model_dump()
    
    # 1. Guardrails Check
    guardrail_results = guardrails.check_inputs(input_data)
    
    # 2. Prediction Model Execution
    try:
        prediction_result = predictor.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")
        
    # 3. Log into Database (SQLite)
    log_prediction(
        db=db,
        features=input_data,
        prediction_result=prediction_result,
        drift_score=guardrail_results['drift_score'],
        is_anomaly=guardrail_results['is_anomaly']
    )
    
    # 4. Formulate Response
    return PredictionResponse(
        prediction=prediction_result['prediction'],
        probability=prediction_result['probability'],
        churn_risk=prediction_result['churn_risk'],
        drift_score=guardrail_results['drift_score'],
        is_anomaly=guardrail_results['is_anomaly'],
        anomalies=guardrail_results['anomalies']
    )

@router.post("/batch")
async def batch_predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload CSV and return Predictions CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        predictions = []
        probabilities = []
        churn_risks = []
        drift_scores = []
        anomalies = []
        
        # Iterate and process
        for _, row in df.iterrows():
            input_dict = row.to_dict()
            guard_res = guardrails.check_inputs(input_dict)
            try:
                pred_res = predictor.predict(input_dict)
                predictions.append(pred_res['prediction'])
                probabilities.append(pred_res['probability'])
                churn_risks.append(pred_res['churn_risk'])
                
                log_prediction(
                    db=db,
                    features=input_dict,
                    prediction_result=pred_res,
                    drift_score=guard_res['drift_score'],
                    is_anomaly=guard_res['is_anomaly']
                )
            except Exception as e:
                predictions.append(-1)
                probabilities.append(0.0)
                churn_risks.append("Error")
            
            drift_scores.append(guard_res['drift_score'])
            anomalies.append(guard_res['is_anomaly'])
            
        df['Prediction'] = predictions
        df['Probability'] = probabilities
        df['Churn_Risk'] = churn_risks
        df['Drift_Score'] = drift_scores
        df['Is_Anomaly'] = anomalies
        
        output = io.StringIO()
        df.to_csv(output, index=False)
        return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=batch_predictions.csv"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")
