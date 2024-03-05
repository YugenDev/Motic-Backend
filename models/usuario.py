from config.database import Base
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)


class UsuarioCreate(Base):
    nombre: str
    email: str
    contraseña: str
