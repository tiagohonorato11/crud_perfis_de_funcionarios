#!/usr/bin/env python3
"""
Script para verificar e criar o usuário admin inicial.
Execute este script se o login admin/admin123 não estiver funcionando.
"""
from app.database import SessionLocal, Base, engine
from app.models import Usuario, CargoUsuario
from app.auth import obter_hash_senha

def criar_admin():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        admin_existente = db.query(Usuario).filter(Usuario.usuario == "admin").first()
        
        if admin_existente:
            print("✅ Usuário admin já existe!")
            print(f"   ID: {admin_existente.id}")
            print(f"   Nome: {admin_existente.nome} {admin_existente.sobrenome}")
            print(f"   Email: {admin_existente.email}")
            print(f"   Cargo: {admin_existente.cargo}")
            
            resposta = input("\n🔄 Deseja resetar a senha para 'admin123'? (s/n): ")
            if resposta.lower() == 's':
                admin_existente.senha_hash = obter_hash_senha("admin123")
                db.commit()
                print("✅ Senha resetada com sucesso!")
        else:
            print("🔧 Criando usuário admin...")
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
            print("✅ Usuário SUPER criado com sucesso!")
            print("   Usuário: admin")
            print("   Senha: admin123")
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("   VERIFICAÇÃO DO USUÁRIO ADMIN")
    print("=" * 50)
    criar_admin()
    print("=" * 50)
