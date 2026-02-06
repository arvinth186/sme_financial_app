import pandas as pd


"""
This file is used to analyze the financial data of all the business types
"""


## Agricultral Industry Analysis

def analyze_agricultural_financials(df: pd.DataFrame):


    total_revenue = float(df["total_revenue"].sum())
    total_expenses = float(df["total_expenses"].sum())

    profit = total_revenue - total_expenses
    profit_margin = profit / total_revenue * 100 if total_revenue > 0 else 0

    avg_inventory_loss_pct = float(df["inventory_loss_percentage"].mean())
    inventory_loss_value = total_revenue * (avg_inventory_loss_pct / 100)
    effective_profit = profit - inventory_loss_value


    cost_pressure_ratio = total_expenses / total_revenue if total_revenue > 0 else 0
    debt_service_ratio = (
        float(df["emi_amount"].mean()) / total_revenue
        if total_revenue > 0 else 0
    )

    # ---- Storage Risk (mode-based) ----
    def calculate_storage_risk(storage_type: str) -> int:
        storage_type = storage_type.lower()
        if storage_type == "open":
            return 80
        elif storage_type == "warehouse":
            return 50
        elif storage_type == "cold_storage":
            return 20
        return 50

    dominant_storage = df["storage_type"].mode()[0]
    storage_risk_score = calculate_storage_risk(dominant_storage)

    season = df["season"].mode()[0]
    primary_crop_type = df["primary_crop_type"].mode()[0]

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin, 2),
        "effective_profit": round(effective_profit, 2),
        "inventory_loss_percentage": round(avg_inventory_loss_pct, 2),
        "inventory_loss_value": round(inventory_loss_value, 2),
        "cost_pressure_ratio": round(cost_pressure_ratio, 2),
        "debt_service_ratio": round(debt_service_ratio, 2),
        "season": str(season),
        "primary_crop_type": str(primary_crop_type),
        "storage_risk_score": storage_risk_score
    }


## Manufacturing Industry Analysis

def analyze_manufacturing_financials(df:pd.DataFrame):

    total_revenue = float(df['total_revenue'].sum())

    total_raw_material_cost = float(df['raw_material_cost'].sum())
    total_labor_cost = float(df['direct_labor_cost'].sum())

    if 'overhead_cost' in df.columns:
        total_overhead_cost = float(df['overhead_cost'].sum())
    else:
        required_overhead_cols = {
            "power_cost",
            "rent_cost",
            "maintenance_cost"
        }

        if required_overhead_cols.issubset(df.columns):
            total_overhead_cost = float(df[list(required_overhead_cols)].sum().sum())
        else:
            missing_cols = required_overhead_cols - set(df.columns)
            raise ValueError(f"Missing required columns for overhead cost calculation. Expected: {required_overhead_cols}")
    
    total_expenses = float(total_raw_material_cost + total_labor_cost + total_overhead_cost)

    profit = float(total_revenue - total_expenses)
    profit_margin = float(profit / total_revenue * 100 if total_revenue > 0 else 0)

    actual_prod = float(df["actual_production"].sum())
    capacity_prod = float(df["production_capacity"].sum())

    capacity_utilization = (
        actual_prod / capacity_prod
        if capacity_prod > 0
        else 0.0
    )

    avg_rm_inventory = float(df["raw_material_inventory_value"].mean())
    avg_wip_inventory = float(df["wip_inventory_value"].mean())
    avg_fg_inventory = float(df["finished_goods_inventory_value"].mean())

    inventory_blockage_ratio = (
        (avg_rm_inventory + avg_wip_inventory + avg_fg_inventory)
        / total_revenue
        if total_revenue > 0
        else 0.0
    )


    cost_efficiency_ratio = total_expenses / total_revenue if total_revenue > 0 else 0.0
    debt_service_ratio = float(df["emi_amount"].mean()) / total_revenue if total_revenue > 0 else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin * 100, 2),

        "capacity_utilization": round(capacity_utilization * 100, 2),
        "inventory_blockage_ratio": round(inventory_blockage_ratio, 2),
        "cost_efficiency_ratio": round(cost_efficiency_ratio, 2),
        "debt_service_ratio": round(debt_service_ratio, 2)
    }
    

# Retail Industry Analysis

import pandas as pd

def analyze_retail_financials(df: pd.DataFrame):

    # ---- Aggregations ----
    total_revenue = float(df["total_revenue"].sum())

    total_cogs = float(df["cost_of_goods_sold"].sum())
    total_store_cost = float(df["store_operating_cost"].sum())
    total_logistics_cost = float(df["logistics_cost"].sum())
    total_loss_cost = float(df["loss_cost"].sum())

    total_expenses = (
        total_cogs +
        total_store_cost +
        total_logistics_cost +
        total_loss_cost
    )

    profit = total_revenue - total_expenses
    profit_margin = profit / total_revenue if total_revenue > 0 else 0

    # ---- Inventory Metrics (Average) ----
    avg_inventory_value = float(df["inventory_value"].mean())

    inventory_blockage_ratio = float(avg_inventory_value / total_revenue)

    inventory_risk_score = (
        float(df["slow_moving_inventory_percentage"].mean()) * 0.6 +
        float(df["expired_inventory_percentage"].mean()) * 0.4
    )

    # ---- Discount & Loss ----
    discount_impact_ratio = float(df["discount_percentage"].mean()) / 100
    loss_cost_ratio = total_loss_cost / total_revenue

    # ---- Debt ----
    debt_service_ratio = float(df["emi_amount"].mean()) / total_revenue

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin * 100, 2),

        "inventory_blockage_ratio": round(inventory_blockage_ratio, 2),
        "inventory_risk_score": round(inventory_risk_score, 2),
        "discount_impact_ratio": round(discount_impact_ratio, 2),
        "loss_cost_ratio": round(loss_cost_ratio, 2),
        "debt_service_ratio": round(debt_service_ratio, 2)
    }


# Logistic Industry Analysis



def analyze_logistics_financials(df: pd.DataFrame):

    # ---- Aggregations ----
    total_revenue = float(df["total_revenue"].sum())

    total_fuel_cost = float(df["fuel_cost"].sum())
    total_driver_wages = float(df["driver_wages"].sum())
    total_vehicle_cost = float(df["vehicle_cost"].sum())
    total_warehouse_cost = float(df["warehouse_cost"].sum())
    total_other_cost = float(df["other_operating_cost"].sum())

    total_expenses = float(
        total_fuel_cost +
        total_driver_wages +
        total_vehicle_cost +
        total_warehouse_cost +
        total_other_cost
    )

    profit = total_revenue - total_expenses
    profit_margin = profit / total_revenue if total_revenue > 0 else 0

    # ---- Logistics Metrics ----
    total_distance = float(df["distance_km"].sum())
    total_shipments = float(df["total_shipments"].sum())

    cost_per_km = float(total_expenses / total_distance if total_distance > 0 else 0)
    revenue_per_shipment = float(total_revenue / total_shipments if total_shipments > 0 else 0)

    fuel_cost_ratio = float(total_fuel_cost / total_expenses if total_expenses > 0 else 0)

    asset_blockage_ratio = float(
        df["avg_goods_in_transit_value"].mean() / total_revenue
        if total_revenue > 0 else 0
    )

    on_time_delivery_percentage = float(df["on_time_delivery_percentage"].mean())

    debt_service_ratio = float(df["emi_amount"].mean() / total_revenue if total_revenue > 0 else 0)

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin * 100, 2),

        "cost_per_km": round(cost_per_km, 2),
        "revenue_per_shipment": round(revenue_per_shipment, 2),
        "fuel_cost_ratio": round(fuel_cost_ratio, 2),
        "asset_blockage_ratio": round(asset_blockage_ratio, 2),
        "on_time_delivery_percentage": round(on_time_delivery_percentage, 2),
        "debt_service_ratio": round(debt_service_ratio, 2)
    }

# Ecommerce Industry Analysis

import pandas as pd

def analyze_ecommerce_financials(df: pd.DataFrame):

    # ---- Aggregations ----
    total_revenue = float(df["total_revenue"].sum())
    total_orders = float(df["orders_count"].sum())

    total_cogs = float(df["cost_of_goods_sold"].sum())
    total_fulfillment = float(df["fulfillment_cost"].sum())
    total_shipping = float(df["shipping_cost"].sum())
    total_payment = float(df["payment_gateway_cost"].sum())
    total_marketing = float(df["marketing_cost"].sum())
    total_returns = float(df["returns_cost"].sum())

    total_expenses = float(
        total_cogs +
        total_fulfillment +
        total_shipping +
        total_payment +
        total_marketing +
        total_returns
    )

    profit = float(total_revenue - total_expenses)
    profit_margin = float(profit / total_revenue if total_revenue > 0 else 0)

    # ---- E-commerce Metrics ----
    contribution_margin = float(
        total_revenue -
        (total_shipping + total_payment + total_returns)
    )

    platform_fee_ratio = float(df["platform_fee_percentage"].mean() / 100)

    inventory_blockage_ratio = float(
        df["inventory_value"].mean() / total_revenue
        if total_revenue > 0 else 0
    )

    order_profitability = float(
        profit / total_orders
        if total_orders > 0 else 0
    )

    return_rate_percentage = float(df["return_rate_percentage"].mean())

    debt_service_ratio = (
        float(df["emi_amount"].mean() / total_revenue)
        if total_revenue > 0 else 0
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "profit_margin": round(profit_margin * 100, 2),

        "contribution_margin": round(contribution_margin, 2),
        "platform_fee_ratio": round(platform_fee_ratio, 2),
        "inventory_blockage_ratio": round(inventory_blockage_ratio, 2),
        "order_profitability": round(order_profitability, 2),
        "return_rate_percentage": round(return_rate_percentage, 2),
        "debt_service_ratio": round(debt_service_ratio, 2)
    }


