from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.registro_emocional import RegistroEmocional, RegistroEmocionalCreate
from typing import List
from pydantic import BaseModel


router = APIRouter()

class registroEmocionalRespuesta(BaseModel):
    fecha: str
    emocion: str
    color: str
    comentario: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registros-emocionales", response_model=registroEmocionalRespuesta)
def crear_registro_emocional(registro_emocional: RegistroEmocionalCreate, db: Session = Depends(get_db)):
    db_registro_emocional = RegistroEmocional(**registro_emocional.dict())
    db.add(db_registro_emocional)
    db.commit()
    db.refresh(db_registro_emocional)
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)

@router.get("/registros-emocionales/{registro_id}", response_model=registroEmocionalRespuesta)
def obtener_registro_emocional(registro_id: int, db: Session = Depends(get_db)):
    db_registro_emocional = db.query(RegistroEmocional).filter(RegistroEmocional.id == registro_id).first()
    if db_registro_emocional is None:
        raise HTTPException(status_code=404, detail="Registro emocional no encontrado")
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)

@router.get("/registros-emocionales/", response_model=List[registroEmocionalRespuesta])
def obtener_registros_emocionales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    registros_emocionales = db.query(RegistroEmocional).offset(skip).limit(limit).all()
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)

@router.put("/registros-emocionales/{registro_id}", response_model=registroEmocionalRespuesta)
def actualizar_registro_emocional(registro_id: int, registro_emocional: RegistroEmocionalCreate, db: Session = Depends(get_db)):
    db_registro_emocional = db.query(RegistroEmocional).filter(RegistroEmocional.id == registro_id).first()
    if db_registro_emocional is None:
        raise HTTPException(status_code=404, detail="Registro emocional no encontrado")
    
    for key, value in db_registro_emocional.dict().items():
        setattr(db_registro_emocional, key, value)

    db.commit()
    db.refresh(db_registro_emocional)
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)


@router.delete("/registros-emocionales/{registro_id}", response_model=registroEmocionalRespuesta)
def eliminar_registro_emocional(registro_id: int, db: Session = Depends(get_db)):
    db_registro_emocional = db.query(RegistroEmocional).filter(RegistroEmocional.id == registro_id).first()
    if db_registro_emocional is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado el registro emocional")
    
    db.delete(db_registro_emocional)
    db.commit()
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)