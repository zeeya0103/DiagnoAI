from pydantic import BaseModel

class ReportResponse(BaseModel):
    hemoglobin: float
    glucose: float
    cholesterol: float
    prediction: str

    class Config:
        from_attributes = True