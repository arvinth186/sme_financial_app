import csv
from io import StringIO
from fastapi.responses import StreamingResponse

AGRICULTURE_COLUMNS = [
    "year",
    "month",
    "season",
    "primary_crop_type",
    "total_revenue",
    "quantity_sold",
    "avg_selling_price",
    "total_expenses",
    "input_cost_percentage",
    "harvested_inventory_quantity",
    "inventory_loss_percentage",
    "storage_type",
    "loan_outstanding_amount",
    "emi_amount",
    "loan_type",
]

MANUFACTURING_COLUMNS = [
    "year",
    "month",

    # Production details
    "product_name",
    "units_produced",
    "units_sold",
    "production_capacity_utilization_percentage",

    # Revenue & pricing
    "total_revenue",
    "avg_selling_price",

    # Cost breakdown
    "raw_material_cost",
    "labor_cost",
    "overhead_cost",
    "total_expenses",

    # Inventory
    "opening_inventory_units",
    "closing_inventory_units",
    "inventory_holding_cost",

    # Quality & efficiency
    "defect_rate_percentage",
    "downtime_hours",

    # Finance
    "loan_outstanding_amount",
    "emi_amount",
    "loan_type",
]

RETAIL_COLUMNS = [
    "year",
    "month",

    # Store & product info
    "store_type",                # e.g., Grocery, Apparel, Electronics
    "product_category",

    # Sales volume
    "units_sold",
    "avg_selling_price",

    # Revenue
    "total_revenue",

    # Cost structure
    "cost_of_goods_sold",        # COGS
    "operational_expenses",      # rent, staff, utilities, marketing
    "total_expenses",

    # Inventory
    "opening_inventory_units",
    "closing_inventory_units",
    "inventory_shrinkage_percentage",

    # Customer metrics
    "footfall_count",
    "conversion_rate_percentage",

    # Pricing & margin
    "discount_percentage",
    "gross_margin_percentage",

    # Finance
    "loan_outstanding_amount",
    "emi_amount",
    "loan_type",
]

LOGISTICS_COLUMNS = [
    "year",
    "month",

    # Fleet & operations
    "vehicle_type",                 # Truck, Van, Bike, Container
    "number_of_vehicles",
    "total_trips",

    # Distance & usage
    "total_distance_km",
    "fuel_consumed_liters",

    # Revenue
    "total_revenue",

    # Cost structure
    "fuel_cost",
    "driver_salary_cost",
    "maintenance_cost",
    "toll_and_permit_cost",
    "warehouse_cost",
    "other_operational_expenses",
    "total_expenses",

    # Delivery performance
    "shipments_delivered",
    "on_time_delivery_percentage",
    "damaged_goods_percentage",

    # Asset health
    "vehicle_downtime_percentage",

    # Finance
    "loan_outstanding_amount",
    "emi_amount",
    "loan_type",
]

ECOMMERCE_COLUMNS = [
    "year",
    "month",

    # Store performance
    "platform",                     # Shopify, Amazon, Flipkart, Custom
    "total_orders",
    "total_units_sold",

    # Revenue
    "gross_sales",                  # Before returns & discounts
    "discount_amount",
    "net_revenue",                  # After discounts, before expenses

    # Marketing
    "marketing_spend",
    "customer_acquisition_cost",
    "conversion_rate_percentage",

    # Fulfillment & operations
    "shipping_cost",
    "packaging_cost",
    "payment_gateway_fees",
    "platform_commission",
    "warehouse_cost",
    "other_operational_expenses",
    "total_expenses",

    # Customer quality
    "return_rate_percentage",
    "refund_amount",
    "average_order_value",

    # Inventory
    "inventory_holding_cost",
    "stock_out_days",

    # Finance
    "loan_outstanding_amount",
    "emi_amount",
    "loan_type",
]




TEMPLATE_MAP = {
    "agriculture": AGRICULTURE_COLUMNS,
    "manufacturing": MANUFACTURING_COLUMNS,
    "retail": RETAIL_COLUMNS,
    "logistics": LOGISTICS_COLUMNS,
    "ecommerce": ECOMMERCE_COLUMNS,
}
