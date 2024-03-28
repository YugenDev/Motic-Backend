from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.registro_emocional import RegistroEmocional, RegistroEmocionalCreate
from models.usuario import Usuario
from typing import List
from pydantic import BaseModel


router = APIRouter()

class registroEmocionalRespuesta(BaseModel):
    usuario_id: int
    fecha: str
    emocion: str
    color: str
    comentario: str

    class Config:
        from_attributes = True
        from_orm = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registros-emocionales/{usuario_id}", response_model=registroEmocionalRespuesta)
def crear_registro_emocional(
    usuario_id: int,
    registro_emocional: RegistroEmocionalCreate,
    db: Session = Depends(get_db)
):
    # Asegúrate de que el usuario exista en la base de datos (puedes agregar lógica adicional si es necesario)
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Asocia el usuario al nuevo registro emocional
    db_registro_emocional = RegistroEmocional(
        usuario_id=usuario_id,
        fecha=registro_emocional.fecha,
        emocion=registro_emocional.emocion,
        color=registro_emocional.color,
        comentario=registro_emocional.comentario
    )

    # Agrega el nuevo registro emocional a la base de datos
    db.add(db_registro_emocional)
    db.commit()
    db.refresh(db_registro_emocional)

    # Devuelve el nuevo registro emocional
    return db_registro_emocional


@router.get("/registros-emocionales/{registro_id}", response_model=registroEmocionalRespuesta)
def obtener_registro_emocional(registro_id: int, db: Session = Depends(get_db)):
    db_registro_emocional = db.query(RegistroEmocional).filter(RegistroEmocional.id == registro_id).first()
    if db_registro_emocional is None:
        raise HTTPException(status_code=404, detail="Registro emocional no encontrado")
    return registroEmocionalRespuesta.from_orm(db_registro_emocional)


@router.get("/registros-emocionales/", response_model=List[registroEmocionalRespuesta])
def obtener_registros_emocionales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    registros_emocionales = db.query(RegistroEmocional).offset(skip).limit(limit).all()
    
    # Convertir los objetos SQLAlchemy en diccionarios
    registros_emocionales_dict = [registro_emocional.__dict__ for registro_emocional in registros_emocionales]
    
    if not registros_emocionales_dict:
        raise HTTPException(status_code=404, detail="No se encontraron registros emocionales")
    
    return registros_emocionales_dict


@router.get("/registros-emocionales/usuario/{usuario_id}", response_model=List[registroEmocionalRespuesta])
def obtener_registros_emocionales_usuario(usuario_id: int, db: Session = Depends(get_db)):
    registros_emocionales = db.query(RegistroEmocional).filter(RegistroEmocional.usuario_id == usuario_id).all()
    
    if not registros_emocionales:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros emocionales para el usuario con ID {usuario_id}")
    
    return registros_emocionales


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