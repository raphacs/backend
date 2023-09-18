import argparse
import os



from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from conexao_banco import DatabaseConnector
from jwt_utils import create_access_token

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev") 

db_connector = DatabaseConnector(environment=environment)

# Configuração da autenticação usando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rota para gerar um token JWT
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
   
    access_token = create_access_token(data={"sub": form_data.username})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/conexao", response_model=dict)
async def verificar_conexao(current_user: str = Depends(oauth2_scheme)):
    try:
        # Tente obter uma engine de conexão com o banco de dados
        engine = db_connector.get_engine()

        # Se a engine foi obtida com sucesso, a conexão está funcionando
        if engine:
            return {"message": "Conexão com o banco de dados está funcionando."}
        else:
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar a conexão: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
