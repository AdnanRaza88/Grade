import csv
import io
import pandas as pd
from fpdf import FPDF
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from app.database import get_session
from app.models import Grade
from app.schemas import GradeResponse

router = APIRouter(prefix="/export", tags=["export"])

def get_all_grades(session: Session) -> list:
    return [GradeResponse.model_validate(g) for g in session.exec(select(Grade)).all()]

@router.get("/csv")
def export_csv(session: Session = Depends(get_session)):
    grades = get_all_grades(session)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "student_name", "father_name", "subject", "marks_obtained", "total_marks", "semester", "date", "exam_type"])
    for g in grades:
        writer.writerow([g.id, g.student_name, g.father_name, g.subject, g.marks_obtained, g.total_marks, g.semester, g.date, g.exam_type])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=grades.csv"})

@router.get("/excel")
def export_excel(session: Session = Depends(get_session)):
    grades = get_all_grades(session)
    df = pd.DataFrame([g.model_dump() for g in grades])
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=grades.xlsx"})

@router.get("/json")
def export_json(session: Session = Depends(get_session)):
    grades = get_all_grades(session)
    return [g.model_dump() for g in grades]

@router.get("/pdf")
def export_pdf(session: Session = Depends(get_session)):
    grades = get_all_grades(session)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="GradePulse - Grades", ln=True, align="C")
    for g in grades:
        pdf.cell(200, 10, txt=f"{g.student_name} - {g.subject}: {g.marks_obtained}/{g.total_marks}", ln=True)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=grades.pdf"})