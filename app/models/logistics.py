from sqlalchemy import Column, Integer, String, Float, DateTime,JSON,ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

"""
This class is used to store the logistics financial analysis results
It is used in the logistics/routes.py file to store the logistics financial analysis results
"""

class LogisticsFinancialAnalysis(Base):
    __tablename__ = "logistics_financial_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    industry = Column(String, default="Logistics")
    year = Column(Integer,nullable=False)
    month = Column(String, nullable=True)

    # ---- Financial Metrics ----
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    profit = Column(Float)
    profit_margin = Column(Float)

    # ---- Logistics-Specific Metrics ----
    cost_per_km = Column(Float)
    revenue_per_shipment = Column(Float)
    fuel_cost_ratio = Column(Float)
    asset_blockage_ratio = Column(Float)
    on_time_delivery_percentage = Column(Float)
    debt_service_ratio = Column(Float)

    # ---- Health & Credit ----
    health_score = Column(Integer)
    health_status = Column(String)
    credit_risk = Column(String)

    # ---- AI Explanation ----
    ai_explanation = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
