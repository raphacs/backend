import argparse
import os



from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm , HTTPBasic, HTTPBasicCredentials

from banco.conexao_banco import DatabaseConnector
from autenticacao.jwt_utils import JWTUtils
from modulos.ingestao_modulos import Ingestor
from properties import Properties

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev") 

db_connector = DatabaseConnector(environment=environment)
ingestor = Ingestor(environment=environment)
properties = Properties(environment=environment)
jwt_utils = JWTUtils(environment=environment)

# Configuração da autenticação usando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

security = HTTPBasic()

def verify_credentials(username: str, password: str):
    expected_username = properties.get("token")["user"]
    expected_password = properties.get("token")["password"]
    return username == expected_username and password == expected_password


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


####ingerindo dados e tratamentos do modulo######

@app.post("/ingerirModulo", response_model=dict)
async def ingerir_modulo(
    module_data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        # Verifique o token JWT recebido
        if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

        # Verifique a conexão com o banco de dados
        engine = db_connector.get_engine()

        if not engine:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

        # Realize a ingestão do módulo
        result = ingestor.inserir_dados(module_data)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ingerir o módulo: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
