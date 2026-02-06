
"""
This file is used to calculate the credit risk of all the business types
"""

# Agriculture Industry Credit Risk

def agriculture_credit_risk(health_score):
    if health_score >= 75:
        return "Low"
    elif health_score >= 50:
        return "Medium"
    return "High"


# Manufacturing Industry Credit Risk
def manufacturing_credit_risk(health_score):
    if health_score >= 75:
        return "Low"
    elif health_score >= 50:
        return "Medium"
    return "High"


# Retail Industry Credit Risk

def retail_credit_risk(health_score):
    if health_score >= 75:
        return "Low"
    elif health_score >= 50:
        return "Medium"
    return "High"


# Logistics Industry Credit Risk

def logistics_credit_risk(health_score):
    if health_score >= 75:
        return "Low"
    elif health_score >= 50:
        return "Medium"
    return "High"


# Ecommerce Industry Credit Risk

def ecommerce_credit_risk(health_score):
    if health_score >= 75:
        return "Low"
    elif health_score >= 50:
        return "Medium"
    return "High"
