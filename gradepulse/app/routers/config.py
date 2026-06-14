import json
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Config
from app.schemas import ConfigUpdate

router = APIRouter(prefix="/config", tags=["config"])

@router.get("/")
def get_config(session: Session = Depends(get_session)):
    configs = session.exec(select(Config)).all()
    return {c.key: c.value for c in configs}

@router.put("/")
def update_config(config: ConfigUpdate, session: Session = Depends(get_session)):
    data = json.loads(config.value)
    for key, value in data.items():
        existing = session.get(Config, key)
        if existing:
            existing.value = str(value)
        else:
            session.add(Config(key=key, value=str(value)))
    session.commit()
    return {"ok": True}