from fastapi import APIRouter, HTTPException
from app.services.templates import TEMPLATE_MAP
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.get("/{industry}")
def download_template(industry: str):
    industry = industry.lower()

    if industry not in TEMPLATE_MAP:
        raise HTTPException(status_code=404, detail="Template not found")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(TEMPLATE_MAP[industry])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={industry}_template.csv"
        },
    )
