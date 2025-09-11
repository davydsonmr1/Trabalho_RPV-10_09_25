# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from ..models import UsuarioLogin, UsuarioCadastro, UsuarioUpdate
from ..auth import get_usuario, gerar_hash, autenticar_usuario, criar_token, get_usuario_atual
from ..database import usuarios
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from ..viacep import buscar_cep
from bson import ObjectId


router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/test")
def test():
    return {"mensagem": "OK, tudo certo!"}

@router.post("/registro")
def registrar(usuariox: UsuarioCadastro):
#def registrar(usuariox: UsuarioCadastro, usuario=Depends(get_usuario_atual)):
    userData = get_usuario(usuariox.username)
    if userData:
        raise HTTPException(status_code=400, detail='Usuário já existe')
    hash_senha = gerar_hash(usuariox.password)

    dadosCep = buscar_cep(usuariox.cep)
    # chamar o viacep
    # adicionar no insert_one os demais dados
    usuarios.insert_one({
        "username":usuariox.username, 
        "password": hash_senha,
        "cep": usuariox.cep,
        "numero": usuariox.numero,
        "complemento": usuariox.complemento,
        "logradouro": dadosCep["logradouro"],
        "bairro": dadosCep["bairro"],
        "localidade": dadosCep["localidade"],
        "uf": dadosCep["uf"],
        })

    return {"mensagem": "Usuário registrado com sucesso!"} 

@router.post("/login")
def logar(usuario: UsuarioLogin):
    autenticado = autenticar_usuario(usuario.username, usuario.password)

    if not autenticado:
        raise HTTPException(status_code=400, detail='Usuário ou Senha Inválidos')

    access_token = criar_token(
        data={"sub":autenticado["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"token": access_token, "expires": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)} 

@router.get("/listarUsuario")
def listar_usuarios(usuario: dict = Depends(get_usuario_atual)):
    lista_usuarios = []
    for usuario in usuarios.find():
        lista_usuarios.append({
            "id": str(usuario["_id"]),
            "username": usuario["username"],
            "cep": usuario["cep"],
            "numero": usuario["numero"],
            "complemento": usuario["complemento"],
            "logradouro": usuario["logradouro"],
            "bairro": usuario["bairro"],
            "localidade": usuario["localidade"],
            "uf": usuario["uf"]
        })
    return lista_usuarios

    @router.put("/atualizarUsuario/{user_id}")
def atualizar_usuario(user_id: str, usuario_update: UsuarioUpdate, usuario_logado: dict = Depends(get_usuario_atual)):
    hash_senha = gerar_hash(usuario_update.password)
    dados_cep = buscar_cep(usuario_update.cep)

    usuarios.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "password": hash_senha,
            "cep": usuario_update.cep,
            "numero": usuario_update.numero,
            "complemento": usuario_update.complemento,
            "logradouro": dados_cep["logradouro"],
            "bairro": dados_cep["bairro"],
            "localidade": dados_cep["localidade"],
            "uf": dados_cep["uf"]
        }}
    )

    return {"mensagem": "Usuário atualizado com sucesso!"}



