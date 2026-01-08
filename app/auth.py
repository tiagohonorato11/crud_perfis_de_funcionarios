from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, models, database

CHAVE_SECRETA = "sua_chave_secreta_super_poderosa"
ALGORITMO = "HS256"
TEMPO_EXPIRACAO_MINUTOS = 30

contexto_senha = CryptContext(schemes=["bcrypt"], deprecated="auto")
esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def verificar_senha(senha_plana, senha_hash):
    return contexto_senha.verify(senha_plana, senha_hash)

def obter_hash_senha(senha):
    return contexto_senha.hash(senha)

def criar_token_acesso(dados: dict, delta_expiracao: Optional[timedelta] = None):
    a_codificar = dados.copy()
    if delta_expiracao:
        expiracao = datetime.utcnow() + delta_expiracao
    else:
        expiracao = datetime.utcnow() + timedelta(minutes=15)
    a_codificar.update({"exp": expiracao})
    jwt_codificado = jwt.encode(a_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)
    return jwt_codificado

async def obter_usuario_logado(token: str = Depends(esquema_oauth2), db: Session = Depends(database.get_db)):
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        nome_usuario: str = payload.get("sub")
        if nome_usuario is None:
            raise excecao_credenciais
        dados_token = schemas.DadosToken(usuario=nome_usuario)
    except JWTError:
        raise excecao_credenciais
    
    usuario = db.query(models.Usuario).filter(models.Usuario.usuario == dados_token.usuario).first()
    if usuario is None:
        raise excecao_credenciais
    return usuario
