

"""
This file is used to recommend financial products to the user based on their credit risk and health score
"""

def recommend_financial_products(industry, credit_risk, health_score, stress_indicators=None):

    products = []

    if credit_risk == "Low":
        products.append("Bank Working Capital Loan")
        products.append("Term Loan at Lower Interest")
        
        if industry == "Manufacturing":
            products.append("Machinery / Equipment Loan")
        if industry == "Logistics":
            products.append("Fleet Expansion Loan")
        if industry == "Ecommerce":
            products.append("Growth Capital / Line of Credit")

    elif credit_risk == "Medium":
        products.append("NBFC Working Capital Loan")
        products.append("Invoice Discounting")

        if industry in ["Retail", "Ecommerce"]:
            products.append("Inventory Financing")
        if industry == "Agriculture":
            products.append("Kisan Credit Card (KCC)")

    else:  # High Risk
        products.append("Secured NBFC Loan")
        products.append("Short-term Working Capital Support")
        products.append("Government-backed Credit Schemes")

    return products
