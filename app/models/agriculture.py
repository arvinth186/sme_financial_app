
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text,ForeignKey
from datetime import datetime
from app.database.db import Base

"""
This class is used to store the agriculture financial analysis results
It is used in the agriculture/routes.py file to store the agriculture financial analysis results
"""

class AgricultureFinancialAnalysis(Base):
    __tablename__ = "agriculture_financial_analysis_results"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    industry = Column(String,default="Agriculture")
    season = Column(String)
    primary_crop_type = Column(String)
    year = Column(Integer,nullable=False)

    # Financial Metrics
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    profit = Column(Float)
    effective_profit = Column(Float)
    profit_margin = Column(Float)

    # Inventory Risk
    inventory_loss_percentage = Column(Float)
    inventory_loss_value = Column(Float)
    storage_risk_score = Column(String)

    # Cost Pressure
    cost_pressure_ratio = Column(Float)
    debt_service_ratio = Column(Float)

    # Health & Credit
    health_score = Column(Float)
    health_status = Column(String)
    credit_risk = Column(String)

    

    ai_explanation = Column(JSON,nullable=True)

    created_at = Column(DateTime,default=datetime.utcnow)


