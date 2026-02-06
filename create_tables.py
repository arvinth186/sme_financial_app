from app.database.db import engine,Base
from app.models.agriculture import AgricultureFinancialAnalysis
from app.models.manufacture import ManufacturingFinancialAnalysis
from app.models.retail import RetailFinancialAnalysis
from app.models.logistics import LogisticsFinancialAnalysis
from app.models.ecommerce import EcommerceFinancialAnalysis
from app.models.user import User

Base.metadata.create_all(bind=engine)

print("Tables created successfully")

