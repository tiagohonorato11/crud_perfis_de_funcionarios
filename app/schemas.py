
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from enum import Enum

class CargoUsuario(str, Enum):
    super = "super"
    gestor = "gestor"
    funcionario = "funcionario"

class UsuarioBase(BaseModel):
    usuario: str
    email: EmailStr
    nome: str
    sobrenome: str
    departamento: str
    cargo: CargoUsuario = CargoUsuario.funcionario
    foto_url: Optional[str] = None
    celular: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioCriacao(UsuarioBase):
    senha: str

class UsuarioAtualizacao(BaseModel):
    senha: Optional[str] = None
    cargo: Optional[CargoUsuario] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    departamento: Optional[str] = None
    celular: Optional[str] = None
    foto_url: Optional[str] = None

class UsuarioResposta(UsuarioBase):
    id: int
    cargo: CargoUsuario

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DadosToken(BaseModel):
    usuario: Optional[str] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
