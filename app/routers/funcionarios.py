from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .. import database, models, schemas, auth

router = APIRouter(
    prefix="/funcionarios",
    tags=["Funcionarios"],
    dependencies=[Depends(auth.obter_usuario_logado)]
)

@router.post("/", response_model=schemas.UsuarioResposta, status_code=status.HTTP_201_CREATED)
def criar_funcionario(
    usuario_in: schemas.UsuarioCriacao, 
    db: Session = Depends(database.get_db), 
    usuario_logado: models.Usuario = Depends(auth.obter_usuario_logado)
):

    if usuario_logado.cargo == models.CargoUsuario.gestor:
        if usuario_in.departamento != usuario_logado.departamento:
            raise HTTPException(status_code=403, detail="Gestores podem criar funcionários apenas do seu departamento.")
    elif usuario_logado.cargo != models.CargoUsuario.super:
        raise HTTPException(status_code=403, detail="Apenas Super ou Gestores podem criar novos funcionários.")
    
    if db.query(models.Usuario).filter(models.Usuario.usuario == usuario_in.usuario).first():
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    if db.query(models.Usuario).filter(models.Usuario.email == usuario_in.email).first():
        raise HTTPException(status_code=400, detail="Email já utilizado.")

    senha_hash = auth.obter_hash_senha(usuario_in.senha)
    novo_usuario = models.Usuario(
        nome=usuario_in.nome,
        sobrenome=usuario_in.sobrenome,
        usuario=usuario_in.usuario,
        departamento=usuario_in.departamento,
        email=usuario_in.email,
        senha_hash=senha_hash,
        cargo=usuario_in.cargo,
        foto_url=usuario_in.foto_url,
        celular=usuario_in.celular
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/", response_model=List[schemas.UsuarioResposta])
def listar_funcionarios(
    pular: int = 0, 
    limite: int = 100, 
    departamento: Optional[str] = None,
    nome: Optional[str] = None,
    db: Session = Depends(database.get_db),
    usuario_logado: models.Usuario = Depends(auth.obter_usuario_logado)
):
    query = db.query(models.Usuario)

    # Regra 2: "super" vê tudo. "gestor" vê departamento. "funcionario" vê a si mesmo.
    if usuario_logado.cargo == models.CargoUsuario.gestor:
        query = query.filter(models.Usuario.departamento == usuario_logado.departamento)
    elif usuario_logado.cargo == models.CargoUsuario.funcionario:
        query = query.filter(models.Usuario.id == usuario_logado.id)
    elif usuario_logado.cargo != models.CargoUsuario.super:
         raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    if departamento and usuario_logado.cargo == models.CargoUsuario.super:
        query = query.filter(models.Usuario.departamento.ilike(f"%{departamento}%"))

    if nome:
        query = query.filter(
            or_(
                models.Usuario.nome.ilike(f"%{nome}%"),
                models.Usuario.sobrenome.ilike(f"%{nome}%")
            )
        )

    usuarios = query.offset(pular).limit(limite).all()
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.UsuarioResposta)
def ler_funcionario(
    usuario_id: int, 
    db: Session = Depends(database.get_db),
    usuario_logado: models.Usuario = Depends(auth.obter_usuario_logado)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    if usuario_logado.cargo == models.CargoUsuario.gestor:
        if usuario.departamento != usuario_logado.departamento:
            raise HTTPException(status_code=403, detail="Acesso negado a funcionários de outro departamento.")
    elif usuario_logado.cargo == models.CargoUsuario.funcionario:
        if usuario.id != usuario_logado.id:
            raise HTTPException(status_code=403, detail="Você só pode visualizar seu próprio perfil.")
    elif usuario_logado.cargo != models.CargoUsuario.super:
        if usuario_logado.id != usuario_id:
             raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    return usuario

@router.put("/{usuario_id}", response_model=schemas.UsuarioResposta)
def atualizar_funcionario(
    usuario_id: int, 
    usuario_update: schemas.UsuarioAtualizacao, 
    db: Session = Depends(database.get_db),
    usuario_logado: models.Usuario = Depends(auth.obter_usuario_logado)
):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    if usuario_logado.cargo == models.CargoUsuario.gestor:
        if usuario_db.departamento != usuario_logado.departamento:
            raise HTTPException(status_code=403, detail="Não pode atualizar funcionários de outro departamento.")
        if usuario_update.departamento and usuario_update.departamento != usuario_logado.departamento:
             raise HTTPException(status_code=403, detail="Gestor não pode mover funcionário para outro departamento.")
    elif usuario_logado.cargo == models.CargoUsuario.funcionario:
        if usuario_id != usuario_logado.id:
            raise HTTPException(status_code=403, detail="Você só pode editar seu próprio perfil.")
    elif usuario_logado.cargo != models.CargoUsuario.super:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    dados_atualizacao = usuario_update.model_dump(exclude_unset=True)
    
    # Proteção: Funcionário não pode mudar seu cargo ou departamento
    if usuario_logado.cargo == models.CargoUsuario.funcionario:
        if 'cargo' in dados_atualizacao:
            del dados_atualizacao['cargo']
        if 'departamento' in dados_atualizacao:
            del dados_atualizacao['departamento']

    for chave, valor in dados_atualizacao.items():
        setattr(usuario_db, chave, valor)
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_funcionario(
    usuario_id: int, 
    db: Session = Depends(database.get_db),
    usuario_logado: models.Usuario = Depends(auth.obter_usuario_logado)
):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    if usuario_logado.cargo == models.CargoUsuario.gestor:
        if usuario_db.departamento != usuario_logado.departamento:
            raise HTTPException(status_code=403, detail="Não pode deletar funcionários de outro departamento.")
    elif usuario_logado.cargo != models.CargoUsuario.super:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    db.delete(usuario_db)
    db.commit()
    return None
