# 🏢 Sistema de Gestão de Colaboradores

Sistema completo de gerenciamento de funcionários (CRUD) desenvolvido com **FastAPI** (backend) e **Vanilla JavaScript** (frontend). O projeto implementa autenticação JWT, controle de acesso baseado em cargos (RBAC), upload de imagens e uma interface moderna e responsiva.

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes Automatizados](#-testes-automatizados)
- [API Endpoints](#-api-endpoints)
- [Controle de Acesso (RBAC)](#-controle-de-acesso-rbac)
- [Capturas de Tela](#-capturas-de-tela)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## ✨ Funcionalidades

### Backend (API REST)

- ✅ **Autenticação JWT** com tokens seguros
- ✅ **CRUD Completo** de funcionários
- ✅ **Controle de Acesso (RBAC)** com 3 níveis:
  - **Super**: Acesso total ao sistema
  - **Gestor**: Gerencia apenas seu departamento
  - **Funcionário**: Visualiza e edita apenas seu próprio perfil
- ✅ **Upload de Fotos** de perfil com armazenamento local
- ✅ **Validação de Dados** com Pydantic
- ✅ **Documentação Interativa** (Swagger UI)
- ✅ **Testes Automatizados** com Pytest

### Frontend (SPA)

- ✅ **Interface Moderna** e responsiva
- ✅ **Navegação SPA** sem recarregamento de página
- ✅ **Filtros Inteligentes** por departamento
- ✅ **Máscara de Celular** automática `(XX)9.XXXX-XXXX`
- ✅ **Visualizador de Fotos** (Lightbox)
- ✅ **Feedback Visual** com modais e validações
- ✅ **Persistência de Estado** com LocalStorage

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados (fácil migração para PostgreSQL/MySQL)
- **Pydantic** - Validação de dados
- **JWT (python-jose)** - Autenticação
- **Passlib + Bcrypt** - Hashing de senhas
- **Pytest** - Testes automatizados

### Frontend

- **HTML5 + CSS3**
- **JavaScript (Vanilla)** - Sem frameworks pesados
- **Google Fonts (Inter)** - Tipografia moderna

---

## 📦 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/tiagohonorato11/desafio_tecnico_perfis_de_funcionarios.git
cd projeto_crud_gestao_funcionarios
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

O servidor estará disponível em: **http://localhost:8000**

> **⚠️ Problema com login?** Se o usuário `admin/admin123` não funcionar:
>
> 1. **Reinstale as dependências** (importante para versões corretas):
>
>    ```bash
>    pip uninstall bcrypt passlib -y
>    pip install -r requirements.txt
>    ```
>
> 2. **Execute o script de verificação**:
>    ```bash
>    python verificar_admin.py
>    ```
>
> Este script irá verificar e recriar o usuário administrador se necessário.

---

## 💻 Como Usar

### Primeiro Acesso

Ao iniciar o sistema pela primeira vez, um usuário administrador é criado automaticamente:

- **Usuário**: `admin`
- **Senha**: `admin123`
- **Cargo**: Super

Use estas credenciais para fazer login e começar a cadastrar outros usuários.

### Navegação

1. **Tela de Login**: Autentique-se com suas credenciais
2. **Dashboard**: Visualize informações gerais
3. **Usuários**: Gerencie funcionários (criar, editar, excluir)
4. **Docs API**: Acesse a documentação interativa do Swagger

### Funcionalidades por Cargo

| Funcionalidade              | Super | Gestor                | Funcionário                  |
| --------------------------- | ----- | --------------------- | ---------------------------- |
| Ver todos os funcionários   | ✅    | ❌ (apenas seu depto) | ❌ (apenas si mesmo)         |
| Criar funcionários          | ✅    | ✅ (apenas seu depto) | ❌                           |
| Editar qualquer funcionário | ✅    | ✅ (apenas seu depto) | ❌                           |
| Editar próprio perfil       | ✅    | ✅                    | ✅ (sem alterar cargo/depto) |
| Excluir funcionários        | ✅    | ✅ (apenas seu depto) | ❌                           |

---

## 📁 Estrutura do Projeto

```
projeto_crud_gestao_funcionarios/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── database.py             # Configuração do banco de dados
│   ├── models.py               # Modelos ORM (SQLAlchemy)
│   ├── schemas.py              # Schemas de validação (Pydantic)
│   ├── auth.py                 # Lógica de autenticação JWT
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Endpoints de autenticação
│   │   ├── funcionarios.py     # Endpoints CRUD de funcionários
│   │   └── upload.py           # Endpoint de upload de imagens
│   │
│   └── static/                 # Arquivos do Frontend
│       ├── index.html
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── api.js          # Funções de comunicação com API
│       │   └── main.js         # Lógica principal do frontend
│       ├── img/
│       └── uploads/            # Fotos de perfil (criado automaticamente)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Configuração de fixtures
│   ├── test_auth.py            # Testes de autenticação
│   └── test_funcionarios.py   # Testes de CRUD e permissões
│
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
└── sql_app.db                  # Banco de dados SQLite (criado automaticamente)
```

---

## 🧪 Testes Automatizados

O projeto inclui uma suíte completa de testes com **Pytest**.

### Executar todos os testes

```bash
pytest
```

### Executar com detalhes

```bash
pytest -v
```

### Cobertura de Testes

- ✅ Autenticação (login sucesso/falha)
- ✅ Criação de funcionários
- ✅ Validação de permissões por cargo
- ✅ Proteção contra alteração não autorizada de cargo
- ✅ Filtros de listagem por departamento

---

## 📡 API Endpoints

### Autenticação

- `POST /login` - Obter token de acesso

### Funcionários

- `GET /funcionarios/` - Listar funcionários (com filtros)
- `POST /funcionarios/` - Criar novo funcionário
- `GET /funcionarios/{id}` - Obter funcionário específico
- `PUT /funcionarios/{id}` - Atualizar funcionário
- `DELETE /funcionarios/{id}` - Excluir funcionário

### Upload

- `POST /upload` - Upload de foto de perfil

### Documentação Completa

Acesse **http://localhost:8000/docs** para ver a documentação interativa completa.

---

## 🔐 Controle de Acesso (RBAC)

O sistema implementa controle de acesso baseado em cargos (Role-Based Access Control):

### Super

- Acesso irrestrito a todos os recursos
- Pode criar, editar e excluir qualquer funcionário
- Pode alterar cargos e departamentos

### Gestor

- Gerencia apenas funcionários do seu departamento
- Pode criar funcionários apenas no seu departamento
- Não pode alterar funcionários de outros departamentos

### Funcionário

- Acesso somente ao próprio perfil
- Pode visualizar e editar informações pessoais
- **Não pode alterar** seu próprio cargo ou departamento (proteção de segurança)

---

## 📸 Capturas de Tela

### Tela de Login

![Login](docs/screenshots/login.png)

### Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### Gestão de Funcionários

![Funcionarios](docs/screenshots/funcionarios.png)

### Modal de Cadastro/Edição

![Modal](docs/screenshots/modal.png)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Tiago Honorato**

---

## 🙏 Agradecimentos

- FastAPI pela excelente documentação
- Comunidade Python pelo suporte
- Todos que contribuíram com feedback

---

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório!**
