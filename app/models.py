from sqlalchemy import Column, Integer, String, Enum
from .database import Base
import enum

class CargoUsuario(str, enum.Enum):
    super = "super"
    gestor = "gestor"
    funcionario = "funcionario"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    sobrenome = Column(String, index=True)
    usuario = Column(String, unique=True, index=True)
    departamento = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    cargo = Column(String)
    foto_url = Column(String, nullable=True)
    celular = Column(String, nullable=True)
