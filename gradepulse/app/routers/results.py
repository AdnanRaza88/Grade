from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Grade
from app.schemas import GradeResponse

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/")
def summary(session: Session = Depends(get_session)):
    grades = session.exec(select(Grade)).all()
    if not grades:
        return {"total_students": 0, "avg_percentage": 0, "total_records": 0, "highest_scorer": "N/A"}
    students = set(g.student_name for g in grades)
    percentages = [(g.marks_obtained / g.total_marks * 100) for g in grades if g.total_marks > 0]
    avg_percent = sum(percentages) / len(percentages) if percentages else 0
    best = max(grades, key=lambda g: (g.marks_obtained / g.total_marks) if g.total_marks > 0 else 0)
    return {
        "total_students": len(students),
        "avg_percentage": round(avg_percent, 2),
        "total_records": len(grades),
        "highest_scorer": best.student_name
    }

@router.get("/{student_name}")
def student_result(student_name: str, session: Session = Depends(get_session)):
    grades = session.exec(select(Grade).where(Grade.student_name == student_name)).all()
    if not grades:
        raise HTTPException(status_code=404, detail="Student not found")
    records = [GradeResponse.model_validate(g) for g in grades]
    total_obtained = sum(g.marks_obtained for g in grades)
    total_total = sum(g.total_marks for g in grades)
    overall = (total_obtained / total_total * 100) if total_total else 0
    return {"student_name": student_name, "records": records, "overall_percentage": round(overall, 2)}