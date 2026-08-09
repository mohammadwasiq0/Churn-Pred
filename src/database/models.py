from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
import os

# Define SQLite DB path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../churn.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PredictionLog(Base):
    """
    Log of all model predictions for monitoring and retraining.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Input Features (Stored as JSON for flexibility, though could be individual columns)
    features = Column(JSON, nullable=False)
    
    # Prediction Results
    prediction = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    churn_risk = Column(String, nullable=False)
    
    # Guardrail Monitoring
    drift_score = Column(Float, nullable=True)
    is_anomaly = Column(Integer, default=0) # 0 = False, 1 = True

# Create tables
Base.metadata.create_all(bind=engine)
