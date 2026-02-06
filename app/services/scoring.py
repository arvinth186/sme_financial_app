
"""
This file is used to calculate the health score of all the business types
"""


def agricultural_health_score(metrics):

    score = 100
    
    if metrics['profit_margin'] < 10:
        score -=25
    if metrics['debt_service_ratio'] > 0.3:
        score -=20
    if metrics['inventory_loss_value'] > 5:
        score -=15
    if metrics['storage_risk_score'] > 60:
        score -=10

    if score >=75:
        status = "Healthy"
    elif score >=50:
        status = "Watch"
    else:
        status = "Stressed"
    
    return score,status


## Manufacturing Industry Scoring

def manufacturing_health_score(metrics):
    score = 100

    if metrics["profit_margin"] < 12:
        score -= 25

    if metrics["capacity_utilization"] < 60:
        score -= 20

    if metrics["inventory_blockage_ratio"] > 0.4:
        score -= 15

    if metrics["debt_service_ratio"] > 0.3:
        score -= 15

    if score >= 75:
        status = "Healthy"
    elif score >= 50:
        status = "Watch"
    else:
        status = "Stressed"

    return score, status


# Retail Industry Scoring

def retail_health_score(metrics):
    score = 100

    if metrics["profit_margin"] < 8:
        score -= 25

    if metrics["inventory_blockage_ratio"] > 0.5:
        score -= 20

    if metrics["inventory_risk_score"] > 30:
        score -= 15

    if metrics["discount_impact_ratio"] > 0.2:
        score -= 10

    if metrics["debt_service_ratio"] > 0.3:
        score -= 15

    if score >= 75:
        status = "Healthy"
    elif score >= 50:
        status = "Watch"
    else:
        status = "Stressed"

    return score, status


# Logistics Industry Scoring
def logistics_health_score(metrics):
    score = 100

    if metrics["profit_margin"] < 10:
        score -= 25

    if metrics["on_time_delivery_percentage"] < 90:
        score -= 20

    if metrics["fuel_cost_ratio"] > 0.4:
        score -= 15

    if metrics["asset_blockage_ratio"] > 0.4:
        score -= 15

    if metrics["debt_service_ratio"] > 0.3:
        score -= 15

    if score >= 75:
        status = "Healthy"
    elif score >= 50:
        status = "Watch"
    else:
        status = "Stressed"

    return score, status

# Ecommerce Industry Scoring

def ecommerce_health_score(metrics):
    score = 100

    # Profitability check
    if metrics["profit_margin"] < 8:
        score -= 25

    # Inventory blockage risk
    if metrics["inventory_blockage_ratio"] > 0.5:
        score -= 20

    # High return rate hurts cash flow
    if metrics["return_rate_percentage"] > 20:
        score -= 15

    # Platform fee pressure
    if metrics["platform_fee_ratio"] > 0.18:
        score -= 10

    # Debt pressure
    if metrics["debt_service_ratio"] > 0.3:
        score -= 15

    # Health status mapping
    if score >= 75:
        status = "Healthy"
    elif score >= 50:
        status = "Watch"
    else:
        status = "Stressed"

    return score, status

    
    