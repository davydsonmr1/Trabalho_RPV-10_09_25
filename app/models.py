# app/models.py
from pydantic import BaseModel

class OperacaoDoisNumeros(BaseModel):
    a:float
    b:float

class OperacaoRaiz(BaseModel):
    numero:float
    indice:float = 2

class Usuario(BaseModel):
    username: str
    password: str
    name: str = None
    email: str = None
    phone: str = None

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioCadastro(BaseModel):
    username: str
    password: str
    cep: str
    numero: str
    complemento: str

class UsuarioUpdate(BaseModel):
    password: str
    cep: str
    numero: str
    complemento: str