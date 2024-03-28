from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.usuario import Usuario, UsuarioCreate
from typing import List
from pydantic import BaseModel
from config import database

router = APIRouter()


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True
        from_orm = True



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    database.Base.metadata.create_all(bind=database.engine)

    db_usuario = Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return UsuarioResponse.from_orm(db_usuario)


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado") 
    return UsuarioResponse.from_orm(db_usuario)

class CredencialesUsuario(BaseModel):
    nombre: str
    contraseña: str

@router.post("/iniciar-sesion")
def obtener_usuario(credenciales: CredencialesUsuario, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.nombre == credenciales.nombre,
        Usuario.contraseña == credenciales.contraseña
    ).first()
    if usuario:
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.model_dump().items():
        setattr(db_usuario, key, value) 

    db.commit()
    db.refresh(db_usuario)
    return UsuarioResponse.from_orm(db_usuario)

@router.delete("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()
    return UsuarioResponse.from_orm(db_usuario)  