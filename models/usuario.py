from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(length=255), index=True)
    email = Column(String(length=255), unique=True, index=True)
    contraseña = Column(String(length=255))

    registros_emocionales = relationship('RegistroEmocional', back_populates='usuario')


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    contraseña: str

    class Config:
        from_attributes = True
        from_orm = True
