from sqlalchemy import Column, Integer, String, Float, DateTime,Text,JSON,ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

"""
This class is used to store the manufacturing financial analysis results
It is used in the manufacturing/routes.py file to store the manufacturing financial analysis results
"""

class ManufacturingFinancialAnalysis(Base):

 
    __tablename__ = "manufacturing_financial_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    industry = Column(String, default="Manufacturing")
    year = Column(Integer,nullable=False)
    month = Column(String, nullable=True)

    # ---- Financial Metrics ----
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    profit = Column(Float)
    profit_margin = Column(Float)

    # ---- Manufacturing Metrics ----
    capacity_utilization = Column(Float)
    inventory_blockage_ratio = Column(Float)
    cost_efficiency_ratio = Column(Float)
    debt_service_ratio = Column(Float)

    # ---- Health & Risk ----
    health_score = Column(Integer)
    health_status = Column(String)
    credit_risk = Column(String)

    # ---- AI Explanation ----
    ai_explanation = Column(JSON,nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
