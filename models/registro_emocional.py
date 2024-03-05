from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class RegistroEmocional(Base):
    __tablename__ = "registros_emocionales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(String)
    emocion = Column(String)
    color = Column(String)
    comentario = Column(String)

    usuario = relationship("Usuario", back_populates="registros_emocionales")


class RegistroEmocionalCreate(BaseModel):
    fecha: str
    emocion: str
    color: str
    comentario: str