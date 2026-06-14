from pydantic import BaseModel
from datetime import date
from typing import Optional

class GradeCreate(BaseModel):
    student_name: str
    father_name: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: int
    date: date
    exam_type: str

class GradeResponse(BaseModel):
    id: int
    student_name: str
    father_name: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: int
    date: date
    exam_type: str

class ConfigUpdate(BaseModel):
    value: str