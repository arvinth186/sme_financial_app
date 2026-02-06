from sqlalchemy import Column, Integer, String, Float, DateTime,JSON,ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

"""
This class is used to store the ecommerce financial analysis results
It is used in the ecommerce/routes.py file to store the ecommerce financial analysis results
"""

class EcommerceFinancialAnalysis(Base):
    __tablename__ = "ecommerce_financial_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    industry = Column(String, default="Ecommerce")
    year = Column(Integer,nullable=False)
    month = Column(String, nullable=True)

    # ---- Financial Metrics ----
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    profit = Column(Float)
    profit_margin = Column(Float)

    # ---- E-commerce Unit Economics ----
    contribution_margin = Column(Float)
    platform_fee_ratio = Column(Float)
    inventory_blockage_ratio = Column(Float)
    order_profitability = Column(Float)
    return_rate_percentage = Column(Float)
    debt_service_ratio = Column(Float)

    # ---- Health & Credit ----
    health_score = Column(Integer)
    health_status = Column(String)
    credit_risk = Column(String)

    # Ai Explanation
    ai_explanation = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
