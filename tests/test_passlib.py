from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    hash_ = pwd_context.hash("teste123")
    print(f"Hash gerado: {hash_}")
    verify = pwd_context.verify("teste123", hash_)
    print(f"Verificação: {verify}")
except Exception as e:
    print(f"Erro no passlib: {e}")
