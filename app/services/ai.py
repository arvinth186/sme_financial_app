from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_factory import get_llm
import json



"""
This file is used to generate the financial explanation for all the business types
"""



llm = get_llm()

def get_language_instruction(language: str | None):
    return {
        "en": "Respond in simple English.",
        "hi": "Respond in simple Hindi using common business terms.",
        "ta": "Respond in simple Tamil using common business terms."
}.get(language, "Respond in simple English.")


# Prompt for Agriculture Financials

prompt_template_agri = ChatPromptTemplate.from_messages([
    (

        "system",
        "{language_instruction} You are a financial advisor for agriculture and farming businesses. "
        "You must respond ONLY in valid JSON.\n\n"
        "CRITICAL WRITING RULES:\n"
        "- Every string MUST follow this pattern:\n"
        "  [fact or metric] + 'which means' + [impact on farmer]\n"
        "- Do NOT write short or generic sentences\n"
        "- Each point must explain WHY it matters to farm income, cash flow, or risk\n"
        "- Imagine explaining to a farmer who asks: 'So what? How does this affect me?'"
    ),
    (
        "human",
        """
IMPORTANT OUTPUT RULES (MANDATORY):
- Respond ONLY with a valid JSON object
- Do NOT include markdown, headings, or extra text
- Do NOT include explanations outside JSON
- All money values must be in Indian Rupees (₹)
- Keep language simple and farmer-friendly
- Return ONLY valid JSON
- If unsure, still return the JSON structure with best possible values

IMPORTANT QUALITY RULE:
If a sentence does NOT explain how it affects the farmer’s money, risk, or stability,
it is INVALID and must be rewritten.

JSON SCHEMA (FOLLOW EXACTLY):

{{
  "Good": ["string", "string", "string"],
  "Risks": ["string", "string"],
  "Improvement": [
    {{
      "action": "string",
      "benefit": "string",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string",
      "benefit": "string",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string",
      "benefit": "string",
      "timeline": "short-term or next season"
    }}
  ],
  "Guidance": "string",
  "ProductRecommendations": {{
    "System": [
      {{
        "product": "string",
        "reason": "string"
      }}
    ],
    "Additional": [
      {{
        "product": "string",
        "reason": "string"
      }}
    ]
  }}
}}

INPUT DATA:

Farm Context:
- Season: {season}
- Crop Type: {primary_crop_type}

Financial Summary:
- Total Revenue: ₹{total_revenue}
- Total Expenses: ₹{total_expenses}
- Profit: ₹{profit}
- Effective Profit: ₹{effective_profit}
- Profit Margin: {profit_margin}%

Operational Risks:
- Inventory Loss: {inventory_loss_percentage}%
- Inventory Loss Value: ₹{inventory_loss_value}
- Storage Risk Score: {storage_risk_score}
- Cost Pressure Ratio: {cost_pressure_ratio}
- EMI Burden Ratio: {debt_service_ratio}

Overall Health:
- Health Score: {health_score}
- Health Status: {health_status}
- Credit Risk: {credit_risk}

SYSTEM-RECOMMENDED PRODUCTS (DO NOT REMOVE):
{products}

INSTRUCTIONS:
- "Good" → 3 clear positive points
- "Risks" → main financial risks
- "Improvement" → EXACTLY 3 items
- "Guidance" → loan & support advice
- "System" → explain ONLY given products
- "Additional" → max 2 different products (optional)
"""
    )
])



def generate_agriculture_financial_explanation(
    metrics,
    health_score,
    health_status,
    credit_risk,
    products,
    language: str = "en"
    ):
    chain = prompt_template_agri | llm
    response = chain.invoke(
        {
            "language_instruction": get_language_instruction(language),
            "season": metrics['season'],
            "primary_crop_type": metrics['primary_crop_type'],
            "total_revenue": metrics['total_revenue'],
            "total_expenses": metrics['total_expenses'],
            "profit": metrics['profit'],
            "effective_profit": metrics['effective_profit'],
            "profit_margin": metrics['profit_margin'],
            "inventory_loss_percentage": metrics['inventory_loss_percentage'],
            "inventory_loss_value": metrics['inventory_loss_value'],
            "storage_risk_score": metrics['storage_risk_score'],
            "cost_pressure_ratio": metrics['cost_pressure_ratio'],
            "debt_service_ratio": metrics['debt_service_ratio'],
            "health_score": health_score,
            "health_status": health_status,
            "credit_risk": credit_risk,
            "products": products
        }
    )
    return json.loads(response.content)


# Prompt for Manufacturing Financials

manufacturing_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "{language_instruction} You are a financial and operations advisor for Manufacturing and MSME factories. "
        "You must respond ONLY in valid JSON.\n\n"
        "CRITICAL WRITING RULES:\n"
        "- Every string MUST explain WHY it matters to factory profit, cash flow, or operations\n"
        "- Follow this pattern: [fact or action] + 'which means' + [impact] + [business outcome]\n"
        "- Do NOT write short or generic statements\n"
        "- Always think like a factory owner concerned about money, machines, and production"
    ),
    (
        "human",
        """
IMPORTANT OUTPUT RULES (MANDATORY):
- Respond ONLY with a valid JSON object
- Do NOT include markdown, headings, or extra text
- All money values must be in Indian Rupees (₹)
- Keep language simple and factory-owner friendly
- If unsure, still return the full JSON structure

JSON SCHEMA (FOLLOW EXACTLY):

{{
  "Good": ["string", "string", "string"],
  "Risks": ["string", "string"],
  "Improvement": [
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, cost, or production impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, cost, or production impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, cost, or production impact)",
      "timeline": "short-term or next season"
    }}
  ],
  "Guidance": "string (30–40 words explaining loan safety, cash flow impact, and risk)",
  "ProductRecommendations": {{
    "System": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining how it helps THIS factory’s cash flow, cost control, or production)"
      }}
    ],
    "Additional": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining future benefit and when it should be used)"
      }}
    ]
  }}
}}

INPUT DATA:

Manufacturing Summary:
- Total Revenue: ₹{total_revenue}
- Total Expenses: ₹{total_expenses}
- Profit: ₹{profit}
- Profit Margin: {profit_margin}%

Operational Efficiency:
- Capacity Utilization: {capacity_utilization}%
- Inventory Blockage Ratio: {inventory_blockage_ratio}
- Cost Efficiency Ratio: {cost_efficiency_ratio}
- EMI Burden Ratio: {debt_service_ratio}

Overall Business Health:
- Health Score: {health_score}
- Health Status: {health_status}
- Credit Risk: {credit_risk}

SYSTEM-RECOMMENDED PRODUCTS (DO NOT REMOVE):
{products}

INSTRUCTIONS:
- "Good" → 3 strong positives with explanation
- "Risks" → clear risks with financial or operational impact
- "Improvement" → EXACTLY 3 deep, actionable steps
- "Guidance" → loan & funding safety advice (30–40 words)
- "System" → explain ONLY given products (30–40 words)
- "Additional" → max 2 different products (optional, 30–40 words)
"""
    )
])


def generate_manufacturing_financial_explanation(
    metrics, 
    health_score, 
    health_status, 
    credit_risk,
    products,
    language: str = "en"
    ):
    chain = manufacturing_prompt_template | llm
    response = chain.invoke(
        {
            "language_instruction": get_language_instruction(language),
            "total_revenue": metrics['total_revenue'],
            "total_expenses": metrics['total_expenses'],
            "profit": metrics['profit'],
            "profit_margin": metrics['profit_margin'],
            "capacity_utilization": metrics['capacity_utilization'],
            "inventory_blockage_ratio": metrics['inventory_blockage_ratio'],
            "cost_efficiency_ratio": metrics['cost_efficiency_ratio'],
            "debt_service_ratio": metrics['debt_service_ratio'],
            "health_score": health_score,
            "health_status": health_status,
            "credit_risk": credit_risk,
            "products":products
        }
    )
    return json.loads(response.content)





# Prompt for Retail Financial Analysis

retail_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "{language_instruction} You are a business and financial advisor for Retail businesses. "
        "You must respond ONLY in valid JSON.\n\n"
        "CRITICAL WRITING RULES:\n"
        "- Every string MUST explain WHY it matters to shop profit, cash flow, or inventory\n"
        "- Follow this pattern: [fact or action] + 'which means' + [impact] + [business outcome]\n"
        "- Do NOT write short or generic statements\n"
        "- Think like a shop owner asking: 'How does this affect my money or stock?'"
    ),
    (
        "human",
        """
IMPORTANT OUTPUT RULES (MANDATORY):
- Respond ONLY with a valid JSON object
- Do NOT include markdown, headings, or extra text
- All money values must be in Indian Rupees (₹)
- Keep language simple and shop-owner friendly
- If unsure, still return the full JSON structure

JSON SCHEMA (FOLLOW EXACTLY):

{{
  "Good": ["string", "string", "string"],
  "Risks": ["string", "string"],
  "Improvement": [
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, stock, or margin impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, stock, or margin impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining cash, stock, or margin impact)",
      "timeline": "short-term or next season"
    }}
  ],
  "Guidance": "string (30–40 words explaining loan safety, cash flow impact, and risk)",
  "ProductRecommendations": {{
    "System": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining how it helps THIS retail business)"
      }}
    ],
    "Additional": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining future benefit and correct usage)"
      }}
    ]
  }}
}}

INPUT DATA:

Retail Performance Summary:
- Total Revenue: ₹{total_revenue}
- Total Expenses: ₹{total_expenses}
- Profit: ₹{profit}
- Profit Margin: {profit_margin}%

Inventory & Pricing Insights:
- Inventory Blockage Ratio: {inventory_blockage_ratio}
- Inventory Risk Score: {inventory_risk_score}
- Discount Impact Ratio: {discount_impact_ratio}
- Loss Cost Ratio: {loss_cost_ratio}

Financial Health:
- EMI Burden Ratio: {debt_service_ratio}
- Health Score: {health_score}
- Health Status: {health_status}
- Credit Risk: {credit_risk}

SYSTEM-RECOMMENDED PRODUCTS (DO NOT REMOVE):
{products}

INSTRUCTIONS:
- "Good" → 3 strong positives about sales, margins, or stock movement
- "Risks" → key risks affecting cash, inventory, or profitability
- "Improvement" → EXACTLY 3 practical shop-level actions
- "Guidance" → loan & funding advice (30–40 words)
- "System" → explain ONLY given products (30–40 words)
- "Additional" → max 2 different products (optional, 30–40 words)
"""
    )
])


def generate_retail_financial_explanation(
    metrics,
    health_score,
    health_status,
    credit_risk,
    products,
    language: str = "en"
    ):
    chain = retail_prompt_template | llm
    response = chain.invoke(
        {
            "language_instruction": get_language_instruction(language),
            "total_revenue": metrics['total_revenue'],
            "total_expenses": metrics['total_expenses'],
            "profit": metrics['profit'],
            "profit_margin": metrics['profit_margin'],
            "inventory_blockage_ratio": metrics['inventory_blockage_ratio'],
            "inventory_risk_score": metrics['inventory_risk_score'],
            "discount_impact_ratio": metrics['discount_impact_ratio'],
            "loss_cost_ratio": metrics['loss_cost_ratio'],
            "debt_service_ratio": metrics['debt_service_ratio'],
            "health_score": health_score,
            "health_status": health_status,
            "credit_risk": credit_risk,
            "products":products
        }
    )
    return json.loads(response.content)



# Prompt for Logistic Financial Analysis

logistics_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "{language_instruction} You are a business and operations advisor for Logistics and Transportation companies. "
        "You must respond ONLY in valid JSON.\n\n"
        "CRITICAL WRITING RULES:\n"
        "- Every string MUST explain WHY it matters to logistics profit, fuel cost, fleet usage, or cash flow\n"
        "- Follow this pattern: [fact or action] + 'which means' + [operational impact] + [financial outcome]\n"
        "- Do NOT write short or generic statements\n"
        "- Think like a fleet owner asking: 'How does this affect my fuel cost, vehicle usage, or cash?'"
    ),
    (
        "human",
        """
IMPORTANT OUTPUT RULES (MANDATORY):
- Respond ONLY with a valid JSON object
- Do NOT include markdown, headings, or extra text
- All money values must be in Indian Rupees (₹)
- Keep language simple and logistics-owner friendly
- If unsure, still return the full JSON structure

JSON SCHEMA (FOLLOW EXACTLY):

{{
  "Good": ["string", "string", "string"],
  "Risks": ["string", "string"],
  "Improvement": [
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining fuel, fleet, or cash impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining fuel, fleet, or cash impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining fuel, fleet, or cash impact)",
      "timeline": "short-term or next season"
    }}
  ],
  "Guidance": "string (30–40 words explaining loan safety, cash flow impact, and risk)",
  "ProductRecommendations": {{
    "System": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining how it helps THIS logistics business)"
      }}
    ],
    "Additional": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining future benefit and correct usage)"
      }}
    ]
  }}
}}

INPUT DATA:

Logistics Performance Summary:
- Total Revenue: ₹{total_revenue}
- Total Expenses: ₹{total_expenses}
- Profit: ₹{profit}
- Profit Margin: {profit_margin}%

Operational Efficiency:
- Cost per KM: ₹{cost_per_km}
- Revenue per Shipment: ₹{revenue_per_shipment}
- On-time Delivery Rate: {on_time_delivery_percentage}%
- Fuel Cost Ratio: {fuel_cost_ratio}

Asset & Cash Flow Indicators:
- Goods-in-Transit Blockage Ratio: {asset_blockage_ratio}
- EMI Burden Ratio: {debt_service_ratio}

Overall Business Health:
- Health Score: {health_score}
- Health Status: {health_status}
- Credit Risk: {credit_risk}

SYSTEM-RECOMMENDED PRODUCTS (DO NOT REMOVE):
{products}

INSTRUCTIONS:
- "Good" → 3 strong positives about revenue, delivery efficiency, or fleet usage
- "Risks" → key risks affecting fuel cost, delays, idle vehicles, or EMI pressure
- "Improvement" → EXACTLY 3 operationally realistic actions
- "Guidance" → loan & funding advice (30–40 words)
- "System" → explain ONLY given products (30–40 words)
- "Additional" → max 2 different products (optional, 30–40 words)
"""
    )
])


def generate_logistics_financial_explanation(
    metrics,
    health_score,
    health_status,
    credit_risk,
    products,
    language: str = "en"
    ):
    chain = logistics_prompt_template | llm
    response = chain.invoke(
        {
            "language_instruction": get_language_instruction(language),
            "total_revenue": metrics['total_revenue'],
            "total_expenses": metrics['total_expenses'],
            "profit": metrics['profit'],
            "profit_margin": metrics['profit_margin'],
            "cost_per_km": metrics['cost_per_km'],
            "revenue_per_shipment": metrics['revenue_per_shipment'],
            "on_time_delivery_percentage": metrics['on_time_delivery_percentage'],
            "fuel_cost_ratio": metrics['fuel_cost_ratio'],
            "asset_blockage_ratio": metrics['asset_blockage_ratio'],
            "debt_service_ratio": metrics['debt_service_ratio'],
            "health_score": health_score,
            "health_status": health_status,
            "credit_risk": credit_risk,
            "products":products
        }
    )
    return json.loads(response.content)


# Ecommerce Financial Analysis

ecommerce_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "{language_instruction} You are a business and financial advisor for E-commerce businesses. "
        "You must respond ONLY in valid JSON.\n\n"
        "CRITICAL WRITING RULES:\n"
        "- Every string MUST explain WHY it matters to profit per order, platform fees, returns, or cash flow\n"
        "- Follow this pattern: [fact or action] + 'which means' + [impact on orders, margin, or cash]\n"
        "- Do NOT write short or generic statements\n"
        "- Think like an online seller asking: 'How does this affect my order profit or money in hand?'"
    ),
    (
        "human",
        """
IMPORTANT OUTPUT RULES (MANDATORY):
- Respond ONLY with a valid JSON object
- Do NOT include markdown, headings, or extra text
- All money values must be in Indian Rupees (₹)
- Keep language simple and online-seller friendly
- If unsure, still return the full JSON structure

JSON SCHEMA (FOLLOW EXACTLY):

{{
  "Good": ["string", "string", "string"],
  "Risks": ["string", "string"],
  "Improvement": [
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining order-level or cash impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining order-level or cash impact)",
      "timeline": "short-term or next season"
    }},
    {{
      "action": "string (2–3 sentences explaining WHAT to do and WHY)",
      "benefit": "string (2–3 sentences explaining order-level or cash impact)",
      "timeline": "short-term or next season"
    }}
  ],
  "Guidance": "string (30–40 words explaining loan safety, cash flow impact, and growth risk)",
  "ProductRecommendations": {{
    "System": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining how it helps THIS e-commerce business)"
      }}
    ],
    "Additional": [
      {{
        "product": "string",
        "reason": "string (30–40 words explaining future benefit and correct usage)"
      }}
    ]
  }}
}}

INPUT DATA:

E-commerce Performance Summary:
- Total Revenue: ₹{total_revenue}
- Total Expenses: ₹{total_expenses}
- Profit: ₹{profit}
- Profit Margin: {profit_margin}%

Unit Economics & Operations:
- Contribution Margin: ₹{contribution_margin}
- Platform Fee Ratio: {platform_fee_ratio}
- Order Profitability: ₹{order_profitability}
- Return Rate: {return_rate_percentage}%
- Inventory Blockage Ratio: {inventory_blockage_ratio}

Financial Health:
- EMI Burden Ratio: {debt_service_ratio}
- Health Score: {health_score}
- Health Status: {health_status}
- Credit Risk: {credit_risk}

SYSTEM-RECOMMENDED PRODUCTS (DO NOT REMOVE):
{products}

INSTRUCTIONS:
- "Good" → 3 strong positives about order profitability, margins, or sales stability
- "Risks" → key risks affecting returns, platform fees, inventory cash blockage
- "Improvement" → EXACTLY 3 practical seller actions
- "Guidance" → funding & growth advice (30–40 words)
- "System" → explain ONLY given products (30–40 words)
- "Additional" → max 2 different products (optional, 30–40 words)
"""
    )
])



def generate_ecommerce_financial_explanation(
    metrics, 
    health_score, 
    health_status, 
    credit_risk,
    products,
    language: str = "en"
    ):
    chain = ecommerce_prompt_template | llm
    response = chain.invoke(
        {
            "language_instruction": get_language_instruction(language),
            "total_revenue": metrics['total_revenue'],
            "total_expenses": metrics['total_expenses'],
            "profit": metrics['profit'],
            "profit_margin": metrics['profit_margin'],
            "contribution_margin": metrics['contribution_margin'],
            "platform_fee_ratio": metrics['platform_fee_ratio'],
            "order_profitability": metrics['order_profitability'],
            "return_rate_percentage": metrics['return_rate_percentage'],
            "inventory_blockage_ratio": metrics['inventory_blockage_ratio'],
            "debt_service_ratio": metrics['debt_service_ratio'],
            "health_score": health_score,
            "health_status": health_status,
            "credit_risk": credit_risk,
            "products":products
        }
    )
    return json.loads(response.content)
