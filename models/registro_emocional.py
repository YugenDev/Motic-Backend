from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class RegistroEmocional(Base):
    __tablename__ = "registros_emocionales"

    id_registro = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(String(length=255))
    emocion = Column(String(length=255))
    color = Column(String(length=255))
    comentario = Column(String(length=255))

    usuario = relationship("Usuario", back_populates="registros_emocionales")


class RegistroEmocionalCreate(BaseModel):
    usuario_id: int
    fecha: str
    emocion: str
    color: str
    comentario: str

    class Config:
        from_attributes = True
        from_orm = True