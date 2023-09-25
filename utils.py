
from fastapi import HTTPException
from autenticacao.jwt_utils import JWTUtils
from banco.conexao_banco import DatabaseConnector
from properties import Properties
import os


environment = os.getenv("ENVIRONMENT", "dev") 

properties = Properties(environment=environment)

db_connector = DatabaseConnector(environment=environment)

jwt_utils = JWTUtils(environment=environment)

def verify_credentials(username: str, password: str):
    expected_username = properties.get("token")["user"]
    expected_password = properties.get("token")["password"]
    return username == expected_username and password == expected_password

def insercao_dados_genericos(current_user,data,dados_func):
    if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

    engine = db_connector.get_engine()

    if not engine:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    # Realize a ingestão do módulo
    result = dados_func(data)

    return result

def atualizacao_dados_genericos(current_user,data,dados_func, chave):
    if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

    engine = db_connector.get_engine()

    if not engine:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    # Realize a ingestão do módulo
    result = dados_func(data, chave)

    return result


def verifica_banco_para_busca(current_user,busca_todos):
    
    if not jwt_utils.verify_token(current_user):
        raise HTTPException(status_code=401, detail="Token inválido")

    engine = db_connector.get_engine()

    if not engine:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    result = busca_todos

    return result

