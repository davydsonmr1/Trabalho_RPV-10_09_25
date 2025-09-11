# readme.md
```
calculadorav6/
| --app/
|  | --__init__.py
|  | --main.py
|  | --config.py
|  | --auth.py
|  | --database.py
|  | --models.py
|  | --routers/
|  |   | -- __init__.py
|  |   | -- calculadora.py
|  |   | -- usuarios.py
|--requirements.txt
|--readme.md
```

Instale as dependências:

pip install -r requirements.txt


Como Rodar a API

python -m uvicorn app.main:app --port 8001 --reload

abra em http://localhost:8001.


Autenticação
POST /usuarios/registro

JSON

{
  "username": "teste",
  "password": "123",
  "cep": "36770001",
  "numero": "123",
  "complemento": "apto 101"
}


POST /usuarios/login

JSON

{
  "username": "teste",
  "password": "123"
}


Usuários
GET /usuarios/

GET http://localhost:8001/usuarios/
Authorization: Bearer <seu_token_aqui>


PUT /usuarios/{user_id}
JSON

{
  "password": "nova_senha",
  "cep": "36770002",
  "numero": "456",
  "complemento": "casa"
}

DELETE /usuarios/{user_id}

