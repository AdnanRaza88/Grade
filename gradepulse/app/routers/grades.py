from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Grade
from app.schemas import GradeCreate, GradeResponse
from typing import List

router = APIRouter(prefix="/grades", tags=["grades"])

@router.post("/", response_model=GradeResponse)
def create_grade(grade: GradeCreate, session: Session = Depends(get_session)):
    db_grade = Grade(**grade.model_dump())
    session.add(db_grade)
    session.commit()
    session.refresh(db_grade)
    return db_grade

@router.get("/", response_model=List[GradeResponse])
def list_grades(session: Session = Depends(get_session)):
    return session.exec(select(Grade)).all()

@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, updated: GradeCreate, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    for key, value in updated.model_dump().items():
        setattr(grade, key, value)
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade

@router.delete("/{grade_id}")
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    session.delete(grade)
    session.commit()
    return {"ok": True}