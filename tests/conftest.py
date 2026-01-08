import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Usuario, CargoUsuario
from app.auth import obter_hash_senha, criar_token_acesso

# Configuração do Banco de Dados de Teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para substituir a dependência de BD
@pytest.fixture(scope="function")
def db_session():
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Fixture do Cliente de Teste
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# Fixtures de Usuários e Tokens
@pytest.fixture
def token_super(db_session):
    """Cria um usuário SUPER e retorna o token de acesso"""
    usuario = Usuario(
        nome="Super", sobrenome="Man", usuario="super",
        email="super@teste.com", departamento="TI",
        cargo=CargoUsuario.super, senha_hash=obter_hash_senha("123")
    )
    db_session.add(usuario)
    db_session.commit()
    return criar_token_acesso({"sub": usuario.usuario})

@pytest.fixture
def token_gestor(db_session):
    """Cria um usuário GESTOR e retorna o token de acesso"""
    usuario = Usuario(
        nome="Gestor", sobrenome="Teste", usuario="gestor",
        email="gestor@teste.com", departamento="Vendas",
        cargo=CargoUsuario.gestor, senha_hash=obter_hash_senha("123")
    )
    db_session.add(usuario)
    db_session.commit()
    return criar_token_acesso({"sub": usuario.usuario})

@pytest.fixture
def token_funcionario(db_session):
    """Cria um usuário FUNCIONARIO e retorna o token de acesso"""
    usuario = Usuario(
        nome="Func", sobrenome="Teste", usuario="func",
        email="func@teste.com", departamento="Vendas",
        cargo=CargoUsuario.funcionario, senha_hash=obter_hash_senha("123")
    )
    db_session.add(usuario)
    db_session.commit()
    return criar_token_acesso({"sub": usuario.usuario})
