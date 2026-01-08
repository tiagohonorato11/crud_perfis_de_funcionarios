from app.models import Usuario, CargoUsuario
from app.auth import obter_hash_senha

def test_login_sucesso(client, db_session):
    # Setup
    user = Usuario(
        nome="Teste", sobrenome="Auth", usuario="authtest",
        email="auth@teste.com", departamento="TI",
        cargo=CargoUsuario.funcionario, senha_hash=obter_hash_senha("senha123")
    )
    db_session.add(user)
    db_session.commit()

    # Execução
    response = client.post("/login", data={"username": "authtest", "password": "senha123"})
    
    # Verificação
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_falha(client):
    response = client.post("/login", data={"username": "errado", "password": "naoexiste"})
    assert response.status_code == 401
