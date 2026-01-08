from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base, SessionLocal
from .models import Usuario, CargoUsuario
from .auth import obter_hash_senha
from .routers import auth, funcionarios, upload
from sqlalchemy.orm import Session
import os
from contextlib import asynccontextmanager

# Define o Lifespan (Startup/Shutdown logic)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas do banco de dados
    Base.metadata.create_all(bind=engine)
    
    # Cria usuario super inicial se não existir
    db = SessionLocal()
    try:
        if not db.query(Usuario).filter(Usuario.cargo == CargoUsuario.super).first():
            print("Criando usuário SUPER inicial...")
            super_usuario = Usuario(
                nome="Admin",
                sobrenome="Super",
                usuario="admin",
                departamento="TI",
                email="admin@empresa.com",
                senha_hash=obter_hash_senha("admin123"),
                cargo=CargoUsuario.super
            )
            db.add(super_usuario)
            db.commit()
            print("Usuário SUPER criado: admin / admin123")
    finally:
        db.close()
    
    yield
    # Shutdown logic (se necessário)

# Inicializa o App com Lifespan
app = FastAPI(
    title="API Gestão Funcionários", 
    description="API para gestão de funcionários",
    lifespan=lifespan
)

# Monta arquivos estáticos para o Frontend
caminho_static = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(caminho_static):
    os.makedirs(caminho_static)

app.mount("/static", StaticFiles(directory=caminho_static), name="static")

# Inclui Routers
app.include_router(auth.router)
app.include_router(funcionarios.router)
app.include_router(upload.router)

# Rota Raiz
@app.get("/", include_in_schema=False)
def root():
    return FileResponse(os.path.join(caminho_static, "index.html"))
