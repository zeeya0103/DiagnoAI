from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
import os

from app.database import get_db
from app.models.report import Report

router = APIRouter(prefix="/reports", tags=["Reports"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================
# UPLOAD REPORT
# ==========================
@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        filename = f"{uuid4()}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(await file.read())

        report = Report(
            user_id=1,
            file_name=file.filename,
            file_path=path,
            prediction="Processing",
            risk="Unknown",
            created_at=datetime.utcnow()
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {"message": "Uploaded", "id": report.id}

    except Exception as e:
        # 🔥 THIS WILL SHOW REAL ERROR IN FRONTEND
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# GET REPORTS
# ==========================
def get_reports(db: Session = Depends(get_db)):
    try:
        return db.query(Report).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))