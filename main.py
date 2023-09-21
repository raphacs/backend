import argparse
import os
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm , HTTPBasic, HTTPBasicCredentials



from banco.conexao_banco import DatabaseConnector
from autenticacao.jwt_utils import JWTUtils
from modulos.modulos import Modulos
from arquivos.arquivos import Arquivos
from usuarios.usuarios import Usuarios
from relatorios.relatorios import Relatorios
from planos.planos import Planos
from clientes.clientes import Clientes
from properties import Properties

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev") 

db_connector = DatabaseConnector(environment=environment)
modulos = Modulos(environment=environment)
arquivos = Arquivos(environment=environment)
usuarios = Usuarios(environment=environment)
relatorio = Relatorios(environment=environment)
properties = Properties(environment=environment)
planos = Planos(environment=environment)
cliente = Clientes(environment=environment)
jwt_utils = JWTUtils(environment=environment)

# Configuração da autenticação usando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

security = HTTPBasic()

def verify_credentials(username: str, password: str):
    expected_username = properties.get("token")["user"]
    expected_password = properties.get("token")["password"]
    return username == expected_username and password == expected_password

def inserir_dados_genericos(current_user,data,inserir_dados_func):
    if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

    engine = db_connector.get_engine()

    if not engine:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    # Realize a ingestão do módulo
    result = inserir_dados_func(data)

    return result


def buscar_dados_genericos(current_user,busca_todos):
    try:
        if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")
   
        engine = db_connector.get_engine()

        if not engine:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
   
        result = busca_todos()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados: {str(e)}")


def busca_parametrizada(current_user, busca_func, aSerBuscado):
    
        # Verifique o token JWT recebido
        if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

        # Verifique a conexão com o banco de dados
        engine = db_connector.get_engine()

        if not engine:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

        # Realize a busca usando a função de busca fornecida
        result = busca_func(aSerBuscado)
        
        print("Resultado da busca:", result)  # Adicione esta linha para depuração

        return result

    



@app.post("/token")
async def get_token(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    
    if not verify_credentials(username, password):
        return None  # Credenciais inválidas
    
    token = jwt_utils.create_access_token(username, password)
    if token:
        return token

    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@app.get("/conexao", response_model=dict)
async def verificar_conexao(current_user: dict = Depends(oauth2_scheme)):
    try:
        # Verifique o token JWT recebido
        if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

        # Tente obter uma engine de conexão com o banco de dados
        engine = db_connector.get_engine()

        # Se a engine foi obtida com sucesso, a conexão está funcionando
        if engine:
            return {"message": "Conexão com o banco de dados está funcionando."}
        else:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar a conexão: {str(e)}")


#### MODULO ######

@app.post("/inserirModulo", response_model=dict)
async def inserir_modulo(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,modulos.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ingerir o módulo: {str(e)}")
    
    
#### ARQUIVO ######

@app.post("/inserirArquivo", response_model=dict)
async def inserir_arquivo(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
       return inserir_dados_genericos(current_user,data,arquivos.inserir_dados)
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ingerir o arquivo: {str(e)}")

#### USUARIO ######

@app.post("/inserirUsuario", response_model=dict)
async def inserir_usuario(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,usuarios.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o usuario: {str(e)}")
    
@app.get("/buscarTodosUsuarios", response_model=list)
async def buscar_usuarios(current_user: dict = Depends(oauth2_scheme)):
    return buscar_dados_genericos(current_user, usuarios.busca_todos)
    
    
@app.get("/buscaPorUsuario/{usuario}", response_model=dict)
async def busca_por_usuario(
    usuario: str,
    current_user: dict = Depends(oauth2_scheme)
):
    # Realize a busca parametrizada
    result = busca_parametrizada(current_user, usuarios.busca_usuario, usuario)
    response_data = {
        "id": result["id"],
        "usuario": result["usuario"],
        "admin": result["admin"]
        
    }

    return response_data
    




#### RELATORIO ######
@app.post("/inserirRelatorio", response_model=dict)
async def inserir_relatorio(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,relatorio.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o usuario: {str(e)}")
   
#### PLANO ###### 
@app.post("/inserirPlano", response_model=dict)
async def inserir_plano(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,planos.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o plano: {str(e)}")

@app.post("/inserirPlanoItem", response_model=dict)
async def inserir_plano_item(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,planos.inserir_dados_itens)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o item do plano: {str(e)}")
   
#### CLIENTE ######
    
@app.post("/inserirCliente", response_model=dict)
async def inserir_cliente(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return inserir_dados_genericos(current_user,data,cliente.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o cliente: {str(e)}")




#### MAIN ######
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
