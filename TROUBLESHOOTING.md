# Correção de Problemas Comuns

## Erro: "password cannot be longer than 72 bytes" ou "bcrypt version"

**Causa**: Incompatibilidade entre versões do `bcrypt` e `passlib`.

**Solução**:

```bash
# 1. Desinstale as versões conflitantes
pip uninstall bcrypt passlib -y

# 2. Reinstale com as versões corretas
pip install -r requirements.txt

# 3. Verifique o usuário admin
python verificar_admin.py
```

## Erro: "No module named 'app'"

**Causa**: Executando o script do diretório errado.

**Solução**:

```bash
# Certifique-se de estar na raiz do projeto
cd projeto_crud_gestao_funcionarios

# Execute o servidor
uvicorn app.main:app --reload
```

## Login não funciona (credenciais corretas)

**Solução**:

1. Verifique se o servidor está rodando em `http://localhost:8000`
2. Abra o console do navegador (F12) e veja se há erros
3. Execute `python verificar_admin.py` para resetar a senha
4. Limpe o cache do navegador (Ctrl+Shift+Del)

## Banco de dados não criado

**Solução**:

```bash
# Delete o banco antigo (se existir)
rm sql_app.db

# Reinicie o servidor (vai criar automaticamente)
uvicorn app.main:app --reload
```
