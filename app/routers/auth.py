from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import database, models, auth, schemas

router = APIRouter(tags=["Autenticacao"])

@router.post("/login", response_model=schemas.Token)
def login_para_token_acesso(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(f"DEBUG: Tentativa de login para usuário '{form_data.username}'")
    usuario = db.query(models.Usuario).filter(models.Usuario.usuario == form_data.username).first()
    
    if not usuario:
        print("DEBUG: Usuário não encontrado no banco.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Usuário encontrado. Verificando senha...")
    senha_valida = auth.verificar_senha(form_data.password, usuario.senha_hash)
    if not senha_valida:
        print("DEBUG: Senha inválida.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print("DEBUG: Login com sucesso!")
    expiracao_token = timedelta(minutes=auth.TEMPO_EXPIRACAO_MINUTOS)
    access_token = auth.criar_token_acesso(
        dados={"sub": usuario.usuario, "cargo": usuario.cargo, "depto": usuario.departamento}, 
        delta_expiracao=expiracao_token
    )
    return {"access_token": access_token, "token_type": "bearer"}
