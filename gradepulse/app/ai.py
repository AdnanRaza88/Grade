import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-key")
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)

STUDY_QUESTIONS = {
    1: "How can I improve my study habits and get higher marks?",
    2: "What are the best revision techniques before an exam?",
    3: "How do I manage time during exams effectively?",
    4: "I am feeling low after bad results, how to stay motivated?",
    5: "How to prepare a study schedule for finals?"
}

def get_study_tip(student_name: str, subject: str, marks: float, total: float, question_id: int) -> str:
    if question_id not in STUDY_QUESTIONS:
        raise ValueError("Invalid question ID")
    question = STUDY_QUESTIONS[question_id]
    prompt = f"Student {student_name} scored {marks}/{total} in {subject}. {question}. Give positive, practical advice in 3-4 sentences."
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

def get_health_tip() -> str:
    prompt = "Give one brief, encouraging health and wellness tip for a student preparing for exams. Keep it under 80 words."
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content