def test_super_cria_funcionario(client, token_super):
    payload = {
        "nome": "Novo",
        "sobrenome": "User",
        "usuario": "novouser",
        "email": "novo@teste.com",
        "senha": "123",
        "departamento": "TI",
        "cargo": "funcionario"
    }
    headers = {"Authorization": f"Bearer {token_super}"}
    response = client.post("/funcionarios/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["usuario"] == "novouser"

def test_gestor_cria_funcionario_mesmo_departamento(client, token_gestor):
    # Gestor é de Vendas (definido no conftest)
    payload = {
        "nome": "Vendedor",
        "sobrenome": "Jr",
        "usuario": "vendedor",
        "email": "vendas@teste.com",
        "senha": "123",
        "departamento": "Vendas",
        "cargo": "funcionario"
    }
    headers = {"Authorization": f"Bearer {token_gestor}"}
    response = client.post("/funcionarios/", json=payload, headers=headers)
    assert response.status_code == 201

def test_gestor_nao_cria_outro_departamento(client, token_gestor):
    # Tenta criar em TI (gestor é de Vendas)
    payload = {
        "nome": "Hacker",
        "sobrenome": "X",
        "usuario": "hacker",
        "email": "hacker@teste.com",
        "senha": "123",
        "departamento": "TI", 
        "cargo": "funcionario"
    }
    headers = {"Authorization": f"Bearer {token_gestor}"}
    response = client.post("/funcionarios/", json=payload, headers=headers)
    assert response.status_code == 403

def test_funcionario_ve_apenas_si_mesmo(client, token_funcionario, token_super):
    # Primeiro criamos outro usuário como Super para ter "ruído" no banco
    client.post("/funcionarios/", json={
        "nome": "Outro", "sobrenome": "Cara", "usuario": "outro",
        "email": "outro@teste.com", "senha": "123", "departamento": "Vendas", "cargo": "funcionario"
    }, headers={"Authorization": f"Bearer {token_super}"})

    # O funcionário logado (func) tenta listar tudo
    headers = {"Authorization": f"Bearer {token_funcionario}"}
    response = client.get("/funcionarios/", headers=headers)
    
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["usuario"] == "func"

def test_funcionario_edita_si_mesmo_mas_nao_muda_cargo(client, token_funcionario, db_session):
    # Descobrir ID do funcionario logado
    from app.models import Usuario
    func_user = db_session.query(Usuario).filter(Usuario.usuario == "func").first()
    
    headers = {"Authorization": f"Bearer {token_funcionario}"}
    
    # Tenta mudar nome e tentar virar SUPER
    payload = {
        "nome": "Nome Alterado",
        "cargo": "super" # Tentativa de golpe
    }
    
    response = client.put(f"/funcionarios/{func_user.id}", json=payload, headers=headers)
    assert response.status_code == 200
    
    # Verifica se nome mudou mas cargo continuou funcionario
    data = response.json()
    assert data["nome"] == "Nome Alterado"
    assert data["cargo"] == "funcionario" # Golpe falhou, segurança funcionou!
