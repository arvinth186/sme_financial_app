import pandas as pd
from fastapi import FastAPI,UploadFile,File,HTTPException,Depends,Query,Form
from sqlalchemy.orm import Session
from app.routes import auth
from sqlalchemy import func



from app.database.deps import get_db  # Dependency to get database session which helps to interact with the database
from app.routes import templates # Import templates router

# LLM Services
from app.services.ai import generate_agriculture_financial_explanation
from app.services.ai import generate_manufacturing_financial_explanation
from app.services.ai import generate_retail_financial_explanation
from app.services.ai import generate_logistics_financial_explanation
from app.services.ai import generate_ecommerce_financial_explanation

# Agricultural Endpoints

from app.services.analysis import analyze_agricultural_financials as analyze_agri_df
from app.services.scoring import agricultural_health_score
from app.services.credit import agriculture_credit_risk
from app.services.persistence import save_agriculture_financial_analysis

from app.models.agriculture import AgricultureFinancialAnalysis


# Manufacturing Endpoints

from app.services.analysis import analyze_manufacturing_financials as analyze_manufacturing_df
from app.services.scoring import manufacturing_health_score
from app.services.credit import manufacturing_credit_risk
from app.services.persistence import save_manufacturing_financial_analysis

from app.models.manufacture import ManufacturingFinancialAnalysis


# Retail Endpoints

from app.services.analysis import analyze_retail_financials as analyze_retail_df
from app.services.scoring import retail_health_score
from app.services.credit import retail_credit_risk
from app.services.persistence import save_retail_financial_analysis

from app.models.retail import RetailFinancialAnalysis


# Logestic Endpoints
from app.services.analysis import analyze_logistics_financials as analyze_logistics_df
from app.services.scoring import logistics_health_score
from app.services.credit import logistics_credit_risk
from app.services.persistence import save_logistics_financial_analysis

from app.models.logistics import LogisticsFinancialAnalysis


# Ecommerce Endpoints
from app.services.analysis import analyze_ecommerce_financials as analyze_ecommerce_df
from app.services.scoring import ecommerce_health_score
from app.services.credit import ecommerce_credit_risk
from app.services.persistence import save_ecommerce_financial_analysis

from app.models.ecommerce import EcommerceFinancialAnalysis


# Products Endpoints
from app.services.products import recommend_financial_products

from fastapi.middleware.cors import CORSMiddleware

ALLOWED_EXTENSIONS = (".csv", ".xlsx")

app = FastAPI(title="SME Financial App", description="SME Financial App", version="1.0.0")
app.include_router(auth.router)
app.include_router(templates.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to the SME Financial App"}




# Agricultural Endpoints

from app.auth.deps import get_current_user
from app.models.user import User


@app.post("/analyze/agricultural")
def analyze_agricultural_financials(file: UploadFile = File(...),db: Session = Depends(get_db),language: str = Form("en"),current_user: User = Depends(get_current_user)):
    
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400,detail="Invalid file type. Please upload a CSV or XLSX file.")
    
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")


    required_columns = {
        "month", "season", "primary_crop_type","year",
        "total_revenue", "quantity_sold", "avg_selling_price",
        "total_expenses", "input_cost_percentage",
        "harvested_inventory_quantity", "inventory_loss_percentage",
        "storage_type",
        "loan_outstanding_amount", "emi_amount", "loan_type"
    }

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise HTTPException(status_code=400,detail=f"Missing columns: {missing}")

    metrics = analyze_agri_df(df)
    year = int(df["year"].iloc[0]) # get the year from the first row

    
    
    health_score,health_status = agricultural_health_score(metrics)

    credit_risk = agriculture_credit_risk(health_score)

    products = recommend_financial_products(
        industry="Agriculture",
        credit_risk=credit_risk,
        health_score=health_score
    )
    products_for_prompt = "\n".join(f"- {p}" for p in products)

    # AI Explanation
    ai_explanation = None
    try:
        ai_explanation = generate_agriculture_financial_explanation(
            metrics,
            health_score,
            health_status,
            credit_risk,
            products_for_prompt,
            language
        )
    except Exception as e:
        print("❌ AI ERROR:", str(e))
        ai_explanation = None
    
    # Save the result to agriculture_financial_analysis_results table
    saved_record = save_agriculture_financial_analysis(
        db=db,
        metrics=metrics,
        year=year,
        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,
        user_id=current_user.id,
        ai_explanation=ai_explanation
        

    )

    return {
        "status": "success",
        "record_id": saved_record.id,
        "industry": "Agriculture",
        "year": year,
        "season": metrics['season'],
        "crop": metrics['primary_crop_type'],

        **metrics,

        "health_score": health_score,
        "health_status": health_status,
        "credit_risk": credit_risk,
        "products": products_for_prompt,
        "ai_explanation": ai_explanation,
        "created_at": saved_record.created_at
    }

# Agriculture GET Endpoints

# 1) For all data

@app.get("/agriculture/analyses")
def get_agriculture_analyses(
    year: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(AgricultureFinancialAnalysis).filter(AgricultureFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(AgricultureFinancialAnalysis.year == year)

    records = (
        query
        .order_by(AgricultureFinancialAnalysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "count": len(records),
        "results": [
            {
                "id": r.id,
                "year": r.year,
                "season": r.season,
                "crop": r.primary_crop_type,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "health_score": r.health_score,
                "health_status": r.health_status,
                "created_at": r.created_at
            }
            for r in records
        ]
    }


# 2) GET agriculture analysis by ID

@app.get("/agriculture/analyses/{analysis_id}")
def get_agriculture_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(AgricultureFinancialAnalysis).filter(
        AgricultureFinancialAnalysis.id == analysis_id,
        AgricultureFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "year": record.year,
        "industry": "Agriculture",
        "season": record.season,
        "crop": record.primary_crop_type,

        "financials": {
            "total_revenue": record.total_revenue,
            "total_expenses": record.total_expenses,
            "profit": record.profit,
            "effective_profit": record.effective_profit,
            "profit_margin": record.profit_margin
        },

        "risks": {
            "inventory_loss_percentage": record.inventory_loss_percentage,
            "inventory_loss_value": record.inventory_loss_value,
            "storage_risk_score": record.storage_risk_score,
            "cost_pressure_ratio": record.cost_pressure_ratio,
            "debt_service_ratio": record.debt_service_ratio
        },

        "health": {
            "health_score": record.health_score,
            "health_status": record.health_status,
            "credit_risk": record.credit_risk
        },

        "ai_explanation": record.ai_explanation,
        "created_at": record.created_at
    }

# 3) GET agriculture dashboard summary (KPIs)

from sqlalchemy import func

@app.get("/agriculture/dashboard")
def agriculture_dashboard(
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(AgricultureFinancialAnalysis).filter(AgricultureFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(AgricultureFinancialAnalysis.year == year)

    total_records = query.count()

    totals = query.with_entities(
        func.sum(AgricultureFinancialAnalysis.total_revenue),
        func.sum(AgricultureFinancialAnalysis.profit),
        func.avg(AgricultureFinancialAnalysis.health_score)
    ).first()

    return {
        "year": year,
        "total_farms_analyzed": total_records,
        "total_revenue": totals[0] or 0,
        "total_profit": totals[1] or 0,
        "average_health_score": round(totals[2], 2) if totals[2] else 0
    }


# 4) GET agriculture AI explanation only

@app.get("/agriculture/analyses/{analysis_id}/ai")
def get_agriculture_ai_explanation(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(AgricultureFinancialAnalysis).filter(
        AgricultureFinancialAnalysis.id == analysis_id,
        AgricultureFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "ai_explanation": record.ai_explanation
    }











# Manufacturing Endpoints

@app.post("/analyze/manufacturing")
def analyze_manufacturing_financials(file: UploadFile = File(...),db: Session = Depends(get_db),language: str = Form("en"),current_user: User = Depends(get_current_user)):

    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        return HTTPException(status_code=400,detail="Invalid file type. Please upload a CSV or XLSX file.")
    
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    
    BASE_REQUIRED_COLUMNS = {
    "month", "product_type","year",
    "production_capacity", "actual_production",
    "total_revenue", "units_sold", "avg_selling_price", "sales_channel",
    "raw_material_cost", "direct_labor_cost",
    "raw_material_inventory_value",
    "wip_inventory_value",
    "finished_goods_inventory_value",
    "loan_outstanding_amount", "emi_amount", "loan_type"
    }

    OVERHEAD_DIRECT = {"overhead_cost"}
    OVERHEAD_SPLIT = {"power_cost", "rent_cost", "maintenance_cost"}

    missing_base = BASE_REQUIRED_COLUMNS - set(df.columns)
    if missing_base:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_base}"
        )

    # Overhead validation
    if not (
        OVERHEAD_DIRECT.issubset(df.columns)
        or OVERHEAD_SPLIT.issubset(df.columns)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Missing overhead cost columns. "
                "Provide either 'overhead_cost' "
                "or all of 'power_cost', 'rent_cost', 'maintenance_cost'."
            )
        )

    metrics = analyze_manufacturing_df(df)
    year = int(df["year"].iloc[0])

    health_score, health_status = manufacturing_health_score(metrics)
    credit_risk = manufacturing_credit_risk(health_score)

    products = recommend_financial_products(
        industry="Manufacturing",
        credit_risk=credit_risk,
        health_score=health_score
    )

    products_for_prompt = "\n".join(f"- {p}" for p in products)

    # AI Explanation
    ai_explanation = None
    try:
        ai_explanation = generate_manufacturing_financial_explanation(
            metrics,
            health_score,
            health_status,
            credit_risk,
            products_for_prompt,
            language
        )
    except Exception:
        ai_explanation = None

    # Save the manufacturing financial analysis results to the database
    saved_record = save_manufacturing_financial_analysis(
        db=db,
        metrics=metrics,
        year=year,
        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,
        user_id=current_user.id,
        ai_explanation=ai_explanation
        
    )

    return {
        "status": "success",
        "record_id": saved_record.id,
        "industry": "Manufacturing",

        **metrics,

        "health_score": health_score,
        "health_status": health_status,
        "credit_risk": credit_risk,
        "products": products,
        "ai_explanation": ai_explanation,
        "created_at": saved_record.created_at
    }


# Manufacture GET Endpoints

@app.get("/manufacturing/analyses")
def get_manufacturing_analyses(
    year: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ManufacturingFinancialAnalysis).filter(ManufacturingFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(ManufacturingFinancialAnalysis.year == year)

    records = (
        query
        .order_by(ManufacturingFinancialAnalysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "count": len(records),
        "results": [
            {
                "id": r.id,
                "year": r.year,
                "industry": r.industry,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "health_score": r.health_score,
                "health_status": r.health_status,
                "created_at": r.created_at
            }
            for r in records
        ]
    }


# 2) GET manufacturing analysis by ID

@app.get("/manufacturing/analyses/{analysis_id}")
def get_manufacturing_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(ManufacturingFinancialAnalysis).filter(
        ManufacturingFinancialAnalysis.id == analysis_id,
        ManufacturingFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "industry": record.industry,
        "year": record.year,

        "financials": {
            "total_revenue": record.total_revenue,
            "total_expenses": record.total_expenses,
            "profit": record.profit,
            "profit_margin": record.profit_margin
        },

        "operations": {
            "capacity_utilization": record.capacity_utilization,
            "inventory_blockage_ratio": record.inventory_blockage_ratio,
            "cost_efficiency_ratio": record.cost_efficiency_ratio,
            "debt_service_ratio": record.debt_service_ratio
        },

        "health": {
            "health_score": record.health_score,
            "health_status": record.health_status,
            "credit_risk": record.credit_risk
        },

        "ai_explanation": record.ai_explanation,
        "created_at": record.created_at
    }

# 3 GET manufacturing dashboard KPIs

from sqlalchemy import func

@app.get("/manufacturing/dashboard")
def manufacturing_dashboard(
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ManufacturingFinancialAnalysis).filter(ManufacturingFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(ManufacturingFinancialAnalysis.year == year)

    total_records = query.count()

    totals = query.with_entities(
        func.sum(ManufacturingFinancialAnalysis.total_revenue),
        func.sum(ManufacturingFinancialAnalysis.profit),
        func.avg(ManufacturingFinancialAnalysis.health_score)
    ).first()

    return {
        "year": year,
        "total_factories_analyzed": total_records,
        "total_revenue": totals[0] or 0,
        "total_profit": totals[1] or 0,
        "average_health_score": round(totals[2], 2) if totals[2] else 0
    }

# 4) GET manufacturing AI explanation

@app.get("/manufacturing/analyses/{analysis_id}/ai")
def get_manufacturing_ai_explanation(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(ManufacturingFinancialAnalysis).filter(
        ManufacturingFinancialAnalysis.id == analysis_id,
        ManufacturingFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "ai_explanation": record.ai_explanation
    }










# Retail Endpoints
@app.post("/analyze/retail")
def analyze_retail_financials(file: UploadFile = File(...),db: Session = Depends(get_db),language: str = Form("en"),current_user: User = Depends(get_current_user)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    required_columns = {
        "month", "store_type", "product_category","year",
        "total_revenue", "quantity_sold", "avg_selling_price",
        "discount_percentage", "sales_channel",
        "cost_of_goods_sold", "store_operating_cost",
        "logistics_cost", "loss_cost",
        "inventory_value",
        "slow_moving_inventory_percentage",
        "expired_inventory_percentage",
        "stock_age_days_avg",
        "loan_outstanding_amount", "emi_amount", "loan_type"
    }

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {required_columns - set(df.columns)}"
        )

    metrics = analyze_retail_df(df)
    year = int(df["year"].iloc[0])

    health_score, health_status = retail_health_score(metrics)
    credit_risk = retail_credit_risk(health_score)

    products = recommend_financial_products(
        industry="Retail",
        credit_risk=credit_risk,
        health_score=health_score
    )

    products_for_prompt = "\n".join(f"- {p}" for p in products)

    # AI Explanation
    ai_explanation = None
    try:
        ai_explanation = generate_retail_financial_explanation(
            metrics,
            health_score,
            health_status,
            credit_risk,
            products_for_prompt,
            language
        )
    except Exception:
        ai_explanation = None
    
    # Save the retail financial analysis results to the database
    saved_record = save_retail_financial_analysis(
        db=db,
        metrics=metrics,
        year=year,
        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,
        user_id=current_user.id,
        ai_explanation=ai_explanation
        
    )

    return {
        "status": "success",
        "record_id": saved_record.id,
        "industry": "Retail",
        **metrics,
        "health_score": health_score,
        "health_status": health_status,
        "credit_risk": credit_risk,
        "products": products,
        "ai_explanation": ai_explanation,
        "created_at": saved_record.created_at
    }


# Retail GET Endpoints

@app.get("/retail/analyses")
def get_retail_analyses(
    year: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(RetailFinancialAnalysis).filter(RetailFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(RetailFinancialAnalysis.year == year)

    records = (
        query
        .order_by(RetailFinancialAnalysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "count": len(records),
        "results": [
            {
                "id": r.id,
                "year": r.year,
                "industry": r.industry,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "health_score": r.health_score,
                "health_status": r.health_status,
                "created_at": r.created_at
            }
            for r in records
        ]
    }


# 2) GET retail analysis by ID

@app.get("/retail/analyses/{analysis_id}")
def get_retail_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(RetailFinancialAnalysis).filter(
        RetailFinancialAnalysis.id == analysis_id,
        RetailFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "industry": record.industry,
        "year": record.year,

        "financials": {
            "total_revenue": record.total_revenue,
            "total_expenses": record.total_expenses,
            "profit": record.profit,
            "profit_margin": record.profit_margin
        },

        "retail_metrics": {
            "inventory_blockage_ratio": record.inventory_blockage_ratio,
            "inventory_risk_score": record.inventory_risk_score,
            "discount_impact_ratio": record.discount_impact_ratio,
            "loss_cost_ratio": record.loss_cost_ratio,
            "debt_service_ratio": record.debt_service_ratio
        },

        "health": {
            "health_score": record.health_score,
            "health_status": record.health_status,
            "credit_risk": record.credit_risk
        },

        "ai_explanation": record.ai_explanation,
        "created_at": record.created_at
    }



# 3) GET retail dashboard KPIs

from sqlalchemy import func

@app.get("/retail/dashboard")
def retail_dashboard(
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(RetailFinancialAnalysis).filter(RetailFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(RetailFinancialAnalysis.year == year)

    total_records = query.count()

    totals = query.with_entities(
        func.sum(RetailFinancialAnalysis.total_revenue),
        func.sum(RetailFinancialAnalysis.profit),
        func.avg(RetailFinancialAnalysis.health_score)
    ).first()

    return {
        "year": year,
        "total_stores_analyzed": total_records,
        "total_revenue": totals[0] or 0,
        "total_profit": totals[1] or 0,
        "average_health_score": round(totals[2], 2) if totals[2] else 0
    }

# 4) GET retail AI Explaination

@app.get("/retail/analyses/{analysis_id}/ai")
def get_retail_ai_explanation(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(RetailFinancialAnalysis).filter(
        RetailFinancialAnalysis.id == analysis_id,
        RetailFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "ai_explanation": record.ai_explanation
    }






#  Logestic Endpoints

@app.post("/analyze/logistics")
def analyze_logistics_financials(file: UploadFile = File(...),db: Session = Depends(get_db),language: str = Form("en"),current_user: User = Depends(get_current_user)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    required_columns = {
        "month", "service_type", "delivery_type","year",
        "total_revenue", "distance_km", "weight_volume", "rate_per_unit", "fuel_surcharge",
        "fuel_cost", "driver_wages", "vehicle_cost", "warehouse_cost", "other_operating_cost",
        "total_shipments", "on_time_delivery_percentage",
        "avg_goods_in_transit_value", "avg_storage_days",
        "loan_outstanding_amount", "emi_amount", "loan_type"
    }

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {required_columns - set(df.columns)}"
        )

    metrics = analyze_logistics_df(df)
    year = int(df["year"].iloc[0])

    health_score, health_status = logistics_health_score(metrics)
    credit_risk = logistics_credit_risk(health_score)

    products = recommend_financial_products(
        industry="Logistics",
        credit_risk=credit_risk,
        health_score=health_score
    )

    products_for_prompt = "\n".join(f"- {p}" for p in products)

    # AI Explanation
    ai_explanation = None
    try:
        ai_explanation = generate_logistics_financial_explanation(
            metrics,
            health_score,
            health_status,
            credit_risk,
            products_for_prompt,
            language
        )
    except Exception:
        ai_explanation = None

    # Save the logistic financial analysis results to the database
    saved_record = save_logistics_financial_analysis(
        db=db,
        metrics=metrics,
        year=year,
        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,
        user_id=current_user.id,
        ai_explanation=ai_explanation
    )

    return {
        "status": "success",
        "record_id": saved_record.id,
        "industry": "Logistics",
        **metrics,
        "health_score": health_score,
        "health_status": health_status,
        "credit_risk": credit_risk,
        "products": products,
        "ai_explanation": ai_explanation,
        "created_at": saved_record.created_at
    }


# Logestic GET Endpoints

#1) GET all logistics analyses

@app.get("/logistics/analyses")
def get_logistics_analyses(
    year: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(LogisticsFinancialAnalysis).filter(LogisticsFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(LogisticsFinancialAnalysis.year == year)

    records = (
        query
        .order_by(LogisticsFinancialAnalysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "count": len(records),
        "results": [
            {
                "id": r.id,
                "year": r.year,
                "industry": r.industry,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "health_score": r.health_score,
                "health_status": r.health_status,
                "created_at": r.created_at
            }
            for r in records
        ]
    }

# 2) GET logistics analysis by ID

@app.get("/logistics/analyses/{analysis_id}")
def get_logistics_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(LogisticsFinancialAnalysis).filter(
        LogisticsFinancialAnalysis.id == analysis_id,
        LogisticsFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "industry": record.industry,
        "year": record.year,

        "financials": {
            "total_revenue": record.total_revenue,
            "total_expenses": record.total_expenses,
            "profit": record.profit,
            "profit_margin": record.profit_margin
        },

        "logistics_metrics": {
            "cost_per_km": record.cost_per_km,
            "revenue_per_shipment": record.revenue_per_shipment,
            "fuel_cost_ratio": record.fuel_cost_ratio,
            "asset_blockage_ratio": record.asset_blockage_ratio,
            "on_time_delivery_percentage": record.on_time_delivery_percentage,
            "debt_service_ratio": record.debt_service_ratio
        },

        "health": {
            "health_score": record.health_score,
            "health_status": record.health_status,
            "credit_risk": record.credit_risk
        },

        "ai_explanation": record.ai_explanation,
        "created_at": record.created_at
    }


# 3) GET logistics dashboard KPIs

from sqlalchemy import func

@app.get("/logistics/dashboard")
def logistics_dashboard(
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(LogisticsFinancialAnalysis).filter(LogisticsFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(LogisticsFinancialAnalysis.year == year)

    total_records = query.count()

    totals = query.with_entities(
        func.sum(LogisticsFinancialAnalysis.total_revenue),
        func.sum(LogisticsFinancialAnalysis.profit),
        func.avg(LogisticsFinancialAnalysis.health_score),
        func.avg(LogisticsFinancialAnalysis.on_time_delivery_percentage)
    ).first()

    return {
        "year": year,
        "total_logistics_companies": total_records,
        "total_revenue": totals[0] or 0,
        "total_profit": totals[1] or 0,
        "average_health_score": round(totals[2], 2) if totals[2] else 0,
        "average_on_time_delivery": round(totals[3], 2) if totals[3] else 0
    }

# 4) GET logistics AI

@app.get("/logistics/analyses/{analysis_id}/ai")
def get_logistics_ai_explanation(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(LogisticsFinancialAnalysis).filter(
        LogisticsFinancialAnalysis.id == analysis_id,
        LogisticsFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "ai_explanation": record.ai_explanation
    }



    
#  Ecommerce Endpoints

@app.post("/analyze/ecommerce")
def analyze_ecommerce_financials(file: UploadFile = File(...),db: Session = Depends(get_db),language: str = Form("en"),current_user: User = Depends(get_current_user)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    required_columns = {
        "month", "seller_type", "product_category", "sales_region","year",
        "total_revenue", "orders_count", "avg_order_value",
        "discount_percentage", "platform_fee_percentage",
        "cost_of_goods_sold", "fulfillment_cost", "shipping_cost",
        "payment_gateway_cost", "marketing_cost", "returns_cost",
        "inventory_value", "stock_age_days_avg", "return_rate_percentage",
        "loan_outstanding_amount", "emi_amount", "loan_type"
    }

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {required_columns - set(df.columns)}"
        )

    metrics = analyze_ecommerce_df(df)
    year = int(df["year"].iloc[0])

    health_score, health_status = ecommerce_health_score(metrics)
    credit_risk = ecommerce_credit_risk(health_score)

    products = recommend_financial_products(
        industry="Ecommerce",
        credit_risk=credit_risk,
        health_score=health_score
    )

    products_for_prompt = "\n".join(f"- {p}" for p in products)

    # AI Explanation
    ai_explanation = None
    try:
        ai_explanation = generate_ecommerce_financial_explanation(
            metrics,
            health_score,
            health_status,
            credit_risk,
            products_for_prompt,
            language
        )
    except Exception:
        ai_explanation = None

    # Save the ecommerce financial analysis results to the database
    saved_record = save_ecommerce_financial_analysis(
        db=db,
        metrics=metrics,
        year=year,
        health_score=health_score,
        health_status=health_status,
        credit_risk=credit_risk,
        user_id=current_user.id,
        ai_explanation=ai_explanation
    )

    return {
        "status": "success",
        "record_id": saved_record.id,
        "industry": "Ecommerce",
        **metrics,
        "health_score": health_score,
        "health_status": health_status,
        "credit_risk": credit_risk,
        "products": products,
        "ai_explanation": ai_explanation,
        "created_at": saved_record.created_at
    }


# GET Ecommerce Endpoints

# 1) GET all e-commerce analyse

@app.get("/ecommerce/analyses")
def get_ecommerce_analyses(
    year: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(EcommerceFinancialAnalysis).filter(EcommerceFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(EcommerceFinancialAnalysis.year == year)

    records = (
        query
        .order_by(EcommerceFinancialAnalysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "count": len(records),
        "results": [
            {
                "id": r.id,
                "year": r.year,
                "industry": r.industry,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "health_score": r.health_score,
                "health_status": r.health_status,
                "created_at": r.created_at
            }
            for r in records
        ]
    }


# 2) GET e-commerce analysis by ID

@app.get("/ecommerce/analyses/{analysis_id}")
def get_ecommerce_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(EcommerceFinancialAnalysis).filter(
        EcommerceFinancialAnalysis.id == analysis_id,
        EcommerceFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "industry": record.industry,
        "year": record.year,

        "financials": {
            "total_revenue": record.total_revenue,
            "total_expenses": record.total_expenses,
            "profit": record.profit,
            "profit_margin": record.profit_margin
        },

        "unit_economics": {
            "contribution_margin": record.contribution_margin,
            "platform_fee_ratio": record.platform_fee_ratio,
            "inventory_blockage_ratio": record.inventory_blockage_ratio,
            "order_profitability": record.order_profitability,
            "return_rate_percentage": record.return_rate_percentage,
            "debt_service_ratio": record.debt_service_ratio
        },

        "health": {
            "health_score": record.health_score,
            "health_status": record.health_status,
            "credit_risk": record.credit_risk
        },

        "ai_explanation": record.ai_explanation,
        "created_at": record.created_at
    }


# 3) GET e-commerce dashboard KPIs

from sqlalchemy import func

@app.get("/ecommerce/dashboard")
def ecommerce_dashboard(
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(EcommerceFinancialAnalysis).filter(EcommerceFinancialAnalysis.user_id == current_user.id)

    if year:
        query = query.filter(EcommerceFinancialAnalysis.year == year)

    total_records = query.count()

    totals = query.with_entities(
        func.sum(EcommerceFinancialAnalysis.total_revenue),
        func.sum(EcommerceFinancialAnalysis.profit),
        func.avg(EcommerceFinancialAnalysis.health_score),
        func.avg(EcommerceFinancialAnalysis.return_rate_percentage)
    ).first()

    return {
        "year": year,
        "total_sellers": total_records,
        "total_revenue": totals[0] or 0,
        "total_profit": totals[1] or 0,
        "average_health_score": round(totals[2], 2) if totals[2] else 0,
        "average_return_rate": round(totals[3], 2) if totals[3] else 0
    }


# 4) GET e-commerce AI explanation

@app.get("/ecommerce/analyses/{analysis_id}/ai")
def get_ecommerce_ai_explanation(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(EcommerceFinancialAnalysis).filter(
        EcommerceFinancialAnalysis.id == analysis_id,
        EcommerceFinancialAnalysis.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "ai_explanation": record.ai_explanation
    }



@app.get("/dashboard")
def dashboard(
    industry: str | None = Query(None),
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    models = {
        "Agriculture": AgricultureFinancialAnalysis,
        "Manufacturing": ManufacturingFinancialAnalysis,
        "Retail": RetailFinancialAnalysis,
        "Logistics": LogisticsFinancialAnalysis,
        "Ecommerce": EcommerceFinancialAnalysis,
    }

    total_analyses = 0
    scores = []

    profit_by_year: dict[int, float] = {}
    revenue_by_year: dict[int, float] = {}
    expenses_by_year: dict[int, float] = {}
    year_breakdown: dict[int, int] = {}
    industry_breakdown = {}
    recent = []

    for name, model in models.items():

        if industry and name != industry:
            continue

        q = db.query(model).filter(model.user_id == current_user.id)

        if year:
            q = q.filter(model.year == year)

        records = q.all()
        industry_breakdown[name] = len(records)
        total_analyses += len(records)

        for r in records:
            scores.append(r.health_score)

            # PROFIT
            profit = r.total_revenue - r.total_expenses
            profit_by_year[r.year] = profit_by_year.get(r.year, 0) + profit

            # REVENUE & EXPENSES
            revenue_by_year[r.year] = revenue_by_year.get(r.year, 0) + r.total_revenue
            expenses_by_year[r.year] = expenses_by_year.get(r.year, 0) + r.total_expenses

            # YEAR COUNT
            year_breakdown[r.year] = year_breakdown.get(r.year, 0) + 1

        recent += (
            q.order_by(model.created_at.desc())
            .limit(5)
            .all()
        )

    return {
        "filters": {
            "industry": industry,
            "year": year,
        },
        "total_analyses": total_analyses,
        "average_health_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "best_health_score": max(scores) if scores else 0,
        "worst_health_score": min(scores) if scores else 0,

        # ✅ CHART DATA
        "profit_by_year": profit_by_year,
        "revenue_by_year": revenue_by_year,
        "expenses_by_year": expenses_by_year,
        "year_breakdown": year_breakdown,
        "industry_breakdown": industry_breakdown,

        "recent_activity": [
            {
                "industry": industry or "Mixed",
                "year": r.year,
                "health_score": r.health_score,
                "created_at": r.created_at,
            }
            for r in recent
        ],
    }
