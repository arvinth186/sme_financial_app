from sqlalchemy import Column, Integer, String, Float, DateTime, JSON,ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

"""
This class is used to store the retail financial analysis results
It is used in the retail/routes.py file to store the retail financial analysis results
"""

class RetailFinancialAnalysis(Base):
    __tablename__ = "retail_financial_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    industry = Column(String, default="Retail")
    year = Column(Integer,nullable=False)
    month = Column(String, nullable=True)

    # ---- Financial Metrics ----
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    profit = Column(Float)
    profit_margin = Column(Float)

    # ---- Retail-Specific Metrics ----
    inventory_blockage_ratio = Column(Float)
    inventory_risk_score = Column(Float)
    discount_impact_ratio = Column(Float)
    loss_cost_ratio = Column(Float)
    debt_service_ratio = Column(Float)

    # ---- Health & Credit ----
    health_score = Column(Integer)
    health_status = Column(String)
    credit_risk = Column(String)

    ai_explanation = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
