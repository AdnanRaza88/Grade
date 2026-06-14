import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Grade
from datetime import date

router = APIRouter(prefix="/upload", tags=["upload"])

def read_upload(file: UploadFile) -> pd.DataFrame:
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["csv", "xlsx"]:
        raise HTTPException(status_code=400, detail="Only CSV/XLSX allowed")
    content = file.file.read()
    if ext == "csv":
        return pd.read_csv(io.BytesIO(content))
    return pd.read_excel(io.BytesIO(content))

@router.post("/preview")
def preview(file: UploadFile = File(...)):
    df = read_upload(file)
    return df.to_dict(orient="records")

@router.post("/validate")
def validate(file: UploadFile = File(...)):
    df = read_upload(file)
    errors = []
    required = ["student_name", "father_name", "subject", "marks_obtained", "total_marks", "semester", "date", "exam_type"]
    for i, row in df.iterrows():
        missing = [col for col in required if col not in row or pd.isna(row[col])]
        if missing:
            errors.append({"row": i + 1, "error": f"Missing {missing}" })
            continue
        try:
            marks = float(row["marks_obtained"])
            total = float(row["total_marks"])
            if marks > total:
                errors.append({"row": i + 1, "error": "Marks > total"})
            if total <= 0:
                errors.append({"row": i + 1, "error": "Total must be positive"})
            int(row["semester"])
        except Exception:
            errors.append({"row": i + 1, "error": "Invalid numeric values"})
    return {"errors": errors, "total_rows": len(df)}

@router.post("/insert")
def insert(file: UploadFile = File(...)):
    df = read_upload(file)
    session = next(get_session())
    inserted = 0
    for _, row in df.iterrows():
        try:
            grade = Grade(
                student_name=str(row["student_name"]),
                father_name=str(row["father_name"]),
                subject=str(row["subject"]),
                marks_obtained=float(row["marks_obtained"]),
                total_marks=float(row["total_marks"]),
                semester=int(row["semester"]),
                date=date.fromisoformat(str(row["date"])[:10]),
                exam_type=str(row["exam_type"])
            )
            session.add(grade)
            inserted += 1
        except Exception:
            continue
    session.commit()
    return {"inserted": inserted}