from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    father_name: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: int
    date: date
    exam_type: str

class Config(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str