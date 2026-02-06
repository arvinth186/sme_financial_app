
from sqlalchemy.orm import Session
from app.models.agriculture import AgricultureFinancialAnalysis
from app.models.manufacture import ManufacturingFinancialAnalysis
from app.models.retail import RetailFinancialAnalysis
from app.models.logistics import LogisticsFinancialAnalysis
from app.models.ecommerce import EcommerceFinancialAnalysis


"""
This file is used to Save the financial data of all the business types in the database
"""


## Agriculture Financial Analysis Persistence

def save_agriculture_financial_analysis(
    db: Session,
    metrics: dict,
    year: int,
    health_score: int,
    health_status: str,
    credit_risk: str,
    user_id: int,
    ai_explanation: str | None = None
):
    record = AgricultureFinancialAnalysis(
        season=metrics["season"],
        primary_crop_type=metrics["primary_crop_type"],
        year=year,
        user_id=user_id,

        total_revenue=metrics["total_revenue"],
        total_expenses=metrics["total_expenses"],
        profit=metrics["profit"],
        effective_profit=metrics["effective_profit"],
        profit_margin=metrics["profit_margin"],

        inventory_loss_percentage=metrics["inventory_loss_percentage"],
        inventory_loss_value=metrics["inventory_loss_value"],
        storage_risk_score=metrics["storage_risk_score"],

        cost_pressure_ratio=metrics["cost_pressure_ratio"],
        debt_service_ratio=metrics["debt_service_ratio"],

        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,

        ai_explanation=ai_explanation,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record



## Manufacturing Financial Analysis Persistence

def save_manufacturing_financial_analysis(
    db: Session,
    metrics: dict,
    year: int,
    health_score: int,
    health_status: str,
    credit_risk: str,
    user_id: int,
    ai_explanation: str | None = None

):
    record = ManufacturingFinancialAnalysis(
        industry="Manufacturing",
        
        year=year,
        user_id=user_id,

        total_revenue=metrics["total_revenue"],
        total_expenses=metrics["total_expenses"],
        profit=metrics["profit"],
        profit_margin=metrics["profit_margin"],

        capacity_utilization=metrics["capacity_utilization"],
        inventory_blockage_ratio=metrics["inventory_blockage_ratio"],
        cost_efficiency_ratio=metrics["cost_efficiency_ratio"],
        debt_service_ratio=metrics["debt_service_ratio"],

        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,

        ai_explanation=ai_explanation
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


## Retail Financial Analysis Persistence

def save_retail_financial_analysis(
    db: Session,
    metrics: dict,
    year: int,
    health_score: int,
    health_status: str,
    credit_risk: str,
    user_id: int,
    ai_explanation: str | None = None,
):

    record = RetailFinancialAnalysis(
        industry="Retail",

        year=year,
        user_id=user_id,

        total_revenue=metrics["total_revenue"],
        total_expenses=metrics["total_expenses"],
        profit=metrics["profit"],
        profit_margin=metrics["profit_margin"],

        inventory_blockage_ratio=metrics["inventory_blockage_ratio"],
        inventory_risk_score=metrics["inventory_risk_score"],
        discount_impact_ratio=metrics["discount_impact_ratio"],
        loss_cost_ratio=metrics["loss_cost_ratio"],
        debt_service_ratio=metrics["debt_service_ratio"],

        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,

        ai_explanation=ai_explanation
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

# Logistics Financial Analysis Persistence

def save_logistics_financial_analysis(
    db: Session, 
    metrics: dict,
    year: int,
    health_score: int,
    health_status: str,
    credit_risk: str,
    user_id: int,
    ai_explanation: str | None = None,
):

    record = LogisticsFinancialAnalysis(
        industry="Logistics",

        year=year,
        user_id=user_id,

        total_revenue=metrics["total_revenue"],
        total_expenses=metrics["total_expenses"],
        profit=metrics["profit"],
        profit_margin=metrics["profit_margin"],

        cost_per_km=metrics["cost_per_km"],
        revenue_per_shipment=metrics["revenue_per_shipment"],
        fuel_cost_ratio=metrics["fuel_cost_ratio"],
        asset_blockage_ratio=metrics["asset_blockage_ratio"],
        on_time_delivery_percentage=metrics["on_time_delivery_percentage"],
        debt_service_ratio=metrics["debt_service_ratio"],

        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,

        ai_explanation=ai_explanation

    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

# Ecommerce Financial Analysis Persistence



def save_ecommerce_financial_analysis(
    db: Session,
    metrics: dict,
    year: int,
    health_score: int,
    health_status: str,
    credit_risk: str,
    user_id: int,
    ai_explanation: str | None = None,
):

    record = EcommerceFinancialAnalysis(


        industry="Ecommerce",

        year=year,
        user_id=user_id,

        total_revenue=metrics["total_revenue"],
        total_expenses=metrics["total_expenses"],
        profit=metrics["profit"],
        profit_margin=metrics["profit_margin"],

        contribution_margin=metrics["contribution_margin"],
        platform_fee_ratio=metrics["platform_fee_ratio"],
        inventory_blockage_ratio=metrics["inventory_blockage_ratio"],
        order_profitability=metrics["order_profitability"],
        return_rate_percentage=metrics["return_rate_percentage"],
        debt_service_ratio=metrics["debt_service_ratio"],

        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,

        ai_explanation=ai_explanation
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


