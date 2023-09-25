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
from utils import  atualizacao_dados_genericos, insercao_dados_genericos, verifica_banco_para_busca, verify_credentials

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev") 



### instanciando classes ######
db_connector = DatabaseConnector(environment=environment)
modulos = Modulos(environment=environment)
arquivos = Arquivos(environment=environment)
usuarios = Usuarios(environment=environment)
relatorios = Relatorios(environment=environment)
properties = Properties(environment=environment)
planos = Planos(environment=environment)
cliente = Clientes(environment=environment)
jwt_utils = JWTUtils(environment=environment)



# Configuração da autenticação usando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()



##### buscando token e conexaoes com o banco
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
        if not jwt_utils.verify_token(current_user):
            raise HTTPException(status_code=401, detail="Token inválido")

        engine = db_connector.get_engine()

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
        return insercao_dados_genericos(current_user, data, modulos.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ingerir o módulo: {str(e)}")
    
    
#### ARQUIVO ######

@app.post("/inserirArquivo", response_model=dict)
async def inserir_arquivo(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
       return insercao_dados_genericos(current_user,data,arquivos.inserir_dados)
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ingerir o arquivo: {str(e)}")
    
    
@app.get("/buscaItem/{dado}", response_model=dict)
async def busca_item(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, arquivos.busca_arquivo(dado) )
    
@app.get("/buscaItemExiste/{dado}", response_model=dict)
async def busca_por_id(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, arquivos.busca_arquivo_existe(dado) )
    


#### USUARIO ######

@app.post("/inserirUsuario", response_model=dict)
async def inserir_usuario(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    try:
        return insercao_dados_genericos(current_user,data,usuarios.inserir_dados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o usuario: {str(e)}")
    
@app.get("/buscarTodosUsuarios", response_model=list)
async def buscar_usuarios(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco_para_busca(current_user, usuarios.busca_todos())


    
    
@app.get("/buscaUsuario/{dado}", response_model=dict)
async def busca_usuario(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, usuarios.busca_usuario(dado) )
    
@app.get("/buscaUsuarioExiste/{usuario}", response_model=dict)
async def busca_por_id(
    usuario: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, usuarios.busca_usuario_existe(usuario) )
    
@app.put("/atualizarUsuario/{usuario}", response_model=dict)
async def atualizar_usuario(
    usuario: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    
    return atualizacao_dados_genericos(current_user,data,usuarios.atualizar_dados, usuario)

    


#### RELATORIO ######
@app.post("/inserirRelatorio", response_model=dict)
async def inserir_relatorio(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,relatorios.inserir_dados)

    
@app.get("/buscarTodosRelatorios", response_model=list)
async def buscar_usuarios(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco_para_busca(current_user, relatorios.busca_todos())
    
    
@app.get("/buscaPorRelatorio/{dado}", response_model=dict)
async def busca_por_usuario(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, relatorios.busca_relatorio(dado) )
    
@app.get("/buscaRelatorioExiste/{dado}", response_model=dict)
async def busca_por_id(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, relatorios.busca_relatorio_existe(dado) )
    
    
   
#### PLANO ###### 
@app.post("/inserirPlano", response_model=dict)
async def inserir_plano(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,planos.inserir_dados)
    

@app.post("/inserirPlanoItem", response_model=dict)
async def inserir_plano_item(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,planos.inserir_dados_itens)

 
@app.get("/buscarTodosPlanos", response_model=list)
async def buscar_planos(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco_para_busca(current_user, planos.busca_todos())
    
    
@app.get("/buscaPlano/{dado}", response_model=dict)
async def busca_plano(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, planos.busca_plano(dado) )

@app.get("/buscaPlanoItem/{dado}", response_model=dict)
async def busca_plano(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, planos.busca_plano_item(dado) )

    
@app.get("/buscaPlanoExiste/{dado}", response_model=dict)
async def busca_plano_existe(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, planos.busca_plano_existe(dado) )
    
   
#### CLIENTE ######
    
@app.post("/inserirCliente", response_model=dict)
async def inserir_cliente(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,cliente.inserir_dados)


@app.get("/buscarTodosClientes", response_model=list)
async def buscar_clientes(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco_para_busca(current_user, cliente.busca_todos())
    
    
@app.get("/buscaCliente/{dado}", response_model=dict)
async def busca_cliente(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, cliente.busca_cliente(dado) )
    
    
@app.get("/buscaClienteExiste/{dado}", response_model=dict)
async def busca_cliente_existe(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco_para_busca(current_user, cliente.busca_cliente_existe(dado) )
    
    


#### MAIN ######
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
