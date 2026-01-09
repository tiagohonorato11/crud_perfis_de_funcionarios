# 🔍 Guia de Troubleshooting

Este guia contém soluções para problemas comuns encontrados durante a instalação e execução do projeto, especialmente em diferentes sistemas e versões de Python.

---

## 1. Erros de Instalação (pip install)

### ❌ Erro: "metadata-generation-failed" ou "Requires Rust/Cargo"

**Causa:** Isso geralmente acontece no **Python 3.13+** quando o `pip` tenta instalar versões antigas de bibliotecas (como Pydantic ou Motor) que não possuem arquivos binários (`wheels`) prontos. Ele tenta compilar do código-fonte, o que exige o compilador Rust.

**Solução:**

1. Verifique se você está usando as versões mais recentes do `requirements.txt`.
2. Certifique-se de que seu `pip` está atualizado:
   ```bash
   python -m pip install --upgrade pip
   ```
3. O repositório foi atualizado para as versões mais recentes das bibliotecas que já suportam Python 3.13 nativamente.

---

## 2. Problemas com Bcrypt e Passlib

### ❌ Erro: "AttributeError: module 'bcrypt' has no attribute '**about**'"

**Causa:** Incompatibilidade entre `passlib` e as versões mais recentes do `bcrypt` (4.x+).

**Solução:**
O projeto fixa o `bcrypt` na versão `3.2.2`. Se o erro persistir, force a reinstalação:

```bash
pip uninstall bcrypt passlib -y
pip install bcrypt==3.2.2 passlib[bcrypt]==1.7.4
```

---

## 3. Banco de Dados e Login Inicial

### ❓ Por que o sistema já veio com dados? (Se clonado antes da correção)

**Causa:** O arquivo `sql_app.db` foi acidentalmente incluído no commit inicial.

**Solução para limpar e começar do zero:**

1. Exclua o arquivo `sql_app.db` localmente.
2. Reinicie o servidor: `uvicorn app.main:app --reload`.
3. O sistema criará um novo banco vazio e inserirá o usuário **admin / admin123** automaticamente.

---

## 4. Comandos de Erro Comuns (Windows)

### ❌ Erro: "uvicorn não é reconhecido"

**Causa:** O ambiente virtual não está ativado ou as dependências não foram instaladas dentro dele.

**Solução:**

1. Ative o venv: `.\venv\Scripts\activate`
2. Instale: `pip install -r requirements.txt`
3. Se o erro persistir, tente rodar via módulo python:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

---

## 5. Script de Verificação Total

Se tudo falhar, execute nosso script de diagnóstico:

```bash
python verificar_admin.py
```

Ele verificará o banco de dados e garantirá que o usuário admin esteja configurado corretamente.
