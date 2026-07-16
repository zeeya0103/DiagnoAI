from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
import os

from app.database import get_db
from app.models.report import Report
from app.models.user import User

from app.services.pdf_parser import PDFParser
from app.services.report_interpreter import ReportInterpreter
from app.services.ml_service import predict_disease

router = APIRouter(prefix="/reports", tags=["Reports"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded"
        )

    filename = f"{uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    # ==========================
    # Extract PDF Text
    # ==========================

    text = PDFParser.extract_text(path)

    print("\n========== PDF TEXT ==========")
    print(text)
    print("==============================\n")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from the PDF."
        )

    # ==========================
    # Extract Parameters
    # ==========================

    values = ReportInterpreter.extract_parameters(text)

    print("\n========== PARAMETERS ==========")
    print(values)
    print("================================\n")

    hb = values.get("hemoglobin")
    glucose = values.get("glucose")

    # ==========================
    # ML Prediction
    # ==========================

    try:

        if hb is not None and glucose is not None:

            prediction = predict_disease(
                hb,
                glucose
            )

        else:

            prediction = "Unable to Predict"

    except Exception as e:

        print("Prediction Error:", e)

        prediction = "Prediction Failed"

    # ==========================
    # Risk Level
    # ==========================

    if prediction in ["Normal", "Healthy"]:
        risk = "Low"

    elif prediction in ["Diabetes", "Diabetes Risk"]:
        risk = "High"

    elif prediction in ["Anaemia", "Anemia", "Anaemia Risk"]:
        risk = "Moderate"

    else:
        risk = "Unknown"

    # ==========================
    # Save Report
    # ==========================

    report = Report(
        file_name=file.filename,
        file_path=path,
        prediction=prediction,
        risk=risk,
        created_at=datetime.utcnow()
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "message": "Report Uploaded Successfully",
        "prediction": prediction,
        "risk": risk,
        "parameters": values,
        "summary": ReportInterpreter.health_summary(values)
    }