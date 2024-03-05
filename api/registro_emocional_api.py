from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.registro_emocional import RegistroEmocional, RegistroEmocionalCreate
from typing import List


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registros-emocionales", response_model=RegistroEmocional)
def crear_registro_emocional(registro_emocional: RegistroEmocionalCreate, db: Session = Depends(get_db)):
    db_registro_emocional = RegistroEmocional(**registro_emocional.dict())
    db.add(db_registro_emocional)
    db.commit()
    db.refresh(db_registro_emocional)
    return db_registro_emocional

@router.get("/registros-emocionales/{registro_id}", response_model=RegistroEmocional)
def obtener_registro_emocional(registro_id: int, db: Session = Depends(get_db)):
    db_registro_emocional = db.query(RegistroEmocional).filter(RegistroEmocional.id == registro_id).first()
    if db_registro_emocional is None:
        raise HTTPException(status_code=404, detail="Registro emocional no encontrado")
    return db_registro_emocional

@router.get("/registros-emocionales/", response_model=List[RegistroEmocional])
def obtener_registros_emocionales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db))
    registros_emocionales = db.query(RegistroEmocional).offset(skip).limit(limit).all()
    return registros_emocionales


@router.put("/registros-emocionales/{registro_id}", response_model=RegistroEmocional)