import argparse
import os
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm , HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder


from banco.conexao_banco import DatabaseConnector
from autenticacao.jwt_utils import JWTUtils
from modulos.modulos import Modulos
from arquivos.arquivos import Arquivos
from usuarios.usuarios import Usuarios
from relatorios.relatorios import Relatorios
from planos.planos import Planos
from clientes.clientes import Clientes
from properties import Properties
from utils import  atualizacao_dados_genericos, insercao_dados_genericos, verifica_banco, verify_credentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ser configurado para a origem específica do seu aplicativo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

environment = os.getenv("ENVIRONMENT", "dev") 



### instanciando classes ######
db_connector = DatabaseConnector(environment=environment)
modulos = Modulos(environment=environment)
arquivos = Arquivos(environment=environment)
usuarios = Usuarios(environment=environment)
relatorios = Relatorios(environment=environment)
properties = Properties(environment=environment)
planos = Planos(environment=environment)
clientes = Clientes(environment=environment)
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
    
    if not jwt_utils.verify_token(current_user):
        raise HTTPException(status_code=401, detail="Token inválido")

    engine = db_connector.get_engine()

    if engine:
        return {"message": "Conexão com o banco de dados está funcionando."}
    else:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

   


#### MODULO ######

@app.post("/inserirModulo", response_model=dict)
async def inserir_modulo(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user, data, modulos.inserir_dados)

    
    
    
@app.get("/buscarTodosModulos", response_model=list)
async def buscar_modulos(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco(current_user, modulos.buscar_todos())
    
    
@app.get("/buscarModulo/{dado}", response_model=dict)
async def buscar_modulo(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, modulos.buscar_modulo(dado) )
    
    
@app.get("/buscarModuloExiste/{dado}", response_model=dict)
async def buscar_modulo_existe(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, modulos.buscar_modulo_existe(dado) )
    
    
    
@app.put("/atualizarModulo/{id}", response_model=dict)
async def atualizar_modulo(
    id: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    return atualizacao_dados_genericos(current_user,data,modulos.atualizar_dados, id)

    
@app.delete("/deletarModulo/{id}", response_model=dict)
async def deletar_modulo(
    id: str,
    current_user: dict = Depends(oauth2_scheme)
):
    result = verifica_banco(current_user, modulos.deletar_modulo(id))

    return result 
    
    
    
#### ARQUIVO ######

@app.post("/inserirArquivo", response_model=dict)
async def inserir_arquivo(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,arquivos.inserir_dados)
        
    
    
@app.get("/buscarArquivo/{cliente}/{dado}", response_model=dict)
async def buscar_arquivo(
    cliente: str,
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, arquivos.buscar_arquivo(cliente, dado) )
    
@app.get("/buscarArquivoExiste/{cliente}/{dado}", response_model=dict)
async def buscar_por_id(
    cliente: str,
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, arquivos.buscar_arquivo_existe(cliente, dado) )

 
@app.put("/atualizarArquivo/{cliente}/{arquivo}", response_model=dict)
async def atualizar_arquivo(
    cliente: str,
    arquivo: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    cliente_arquivo = {"cliente": cliente, "arquivo": arquivo}
    return atualizacao_dados_genericos(current_user,data,arquivos.atualizar_dados, cliente_arquivo)

    
@app.delete("/deletarArquivo/{cliente}/{arquivo}", response_model=dict)
async def deletar_arquivo(
    cliente: str,
    arquivo: str,
    current_user: dict = Depends(oauth2_scheme)
):
    cliente_arquivo = {"cliente": cliente, "arquivo": arquivo}
    result = verifica_banco(current_user, arquivos.deletar_arquivo(cliente_arquivo))

    return result

#### USUARIO ######

@app.post("/inserirUsuario", response_model=dict)
async def inserir_usuario(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,usuarios.inserir_dados)

    
    
@app.get("/buscarTodosUsuarios", response_model=list)
async def buscar_usuarios(current_user: dict = Depends(oauth2_scheme)):
    
    
    return verifica_banco(current_user, usuarios.buscar_todos())


    
    
@app.get("/buscarUsuario/{dado}", response_model=dict)
async def buscar_usuario(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, usuarios.buscar_usuario(dado) )

    
@app.get("/buscarUsuarioExiste/{usuario}", response_model=dict)
async def buscar_por_id(
    usuario: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, usuarios.buscar_usuario_existe(usuario) )
    
@app.put("/atualizarUsuario/{usuario}", response_model=dict)
async def atualizar_usuario(
    usuario: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    
    return atualizacao_dados_genericos(current_user,data,usuarios.atualizar_dados, usuario)

    
@app.delete("/deletarUsuario/{usuario}", response_model=dict)
async def deletar_usuario(
    usuario: str,
    current_user: dict = Depends(oauth2_scheme)
):
    
    result = verifica_banco(current_user, usuarios.deletar_usuario(usuario))

    return result

    

#### RELATORIO ######
@app.post("/inserirRelatorio", response_model=dict)
async def inserir_relatorio(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,relatorios.inserir_dados)

    
@app.get("/buscarTodosRelatorios", response_model=list)
async def buscar_relatorios(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco(current_user, relatorios.buscar_todos())
    
    
@app.get("/buscarPorRelatorio/{dado}", response_model=dict)
async def buscar_por_relatorio(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, relatorios.buscar_relatorio(dado) )
    
@app.get("/buscarelatorioExiste/{dado}", response_model=dict)
async def buscar_por_id(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, relatorios.buscar_relatorio_existe(dado) )
    
    
    
@app.put("/atualizarRelatorio/{relatorio}", response_model=dict)
async def atualizar_relatorio(
    relatorio: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    
    return atualizacao_dados_genericos(current_user,data,relatorios.atualizar_dados, relatorio)


@app.delete("/deletarRelatorio/{relatorio}", response_model=dict)
async def deletar_relatorio(
    relatorio: str,
    current_user: dict = Depends(oauth2_scheme)
):
    
    result = verifica_banco(current_user, relatorios.deletar_usuario(relatorio))

    return result
   
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
    
    return verifica_banco(current_user, planos.buscar_todos())
    
    
@app.get("/buscarPlano/{dado}", response_model=dict)
async def buscar_plano(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, planos.buscar_plano(dado) )

@app.get("/buscarTodosPlanosItem/{id}", response_model=list)
async def buscar_plano_itens(
    id: str,
    current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco(current_user, planos.buscar_plano_itens(id))
    

    
@app.get("/buscarPlanoExiste/{dado}", response_model=dict)
async def buscar_plano_existe(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, planos.buscar_plano_existe(dado) )
  
  
@app.put("/atualizarPlano/{plano}", response_model=dict)
async def atualizar_plano(
    plano: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    
    return atualizacao_dados_genericos(current_user,data,planos.atualizar_dados, plano)

    
@app.delete("/deletarPlano/{plano}", response_model=dict)
async def deletar_plano(
    plano: str,
    current_user: dict = Depends(oauth2_scheme)
):
    
    result = verifica_banco(current_user, planos.deletar_plano(plano))

    return result

  
@app.put("/atualizarPlanoItem/{plano}", response_model=dict)
async def atualizar_plano_item(
    plano: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    
    return atualizacao_dados_genericos(current_user,data,planos.atualizar_item_plano, plano)

    
@app.delete("/deletarPlanoItem/{plano}", response_model=dict)
async def deletar_plano_item(
    plano: str,
    current_user: dict = Depends(oauth2_scheme)
):
    
    result = verifica_banco(current_user, planos.deletar_plano_item(plano))

    return result

  
  
    
   
#### CLIENTE ######
    
@app.post("/inserirCliente", response_model=dict)
async def inserir_cliente(
    data: dict,
    current_user: dict = Depends(oauth2_scheme)
):
    
    return insercao_dados_genericos(current_user,data,clientes.inserir_dados)


@app.get("/buscarTodosClientes", response_model=list)
async def buscar_clientes(current_user: dict = Depends(oauth2_scheme)):
    
    return verifica_banco(current_user, clientes.buscar_todos())
    
    
@app.get("/buscarCliente/{dado}", response_model=dict)
async def buscar_cliente(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, clientes.buscar_cliente(dado) )
    
    
@app.get("/buscarClienteExiste/{dado}", response_model=dict)
async def buscar_cliente_existe(
    dado: str,
    current_user: dict = Depends(oauth2_scheme)
):

    return verifica_banco(current_user, clientes.buscar_cliente_existe(dado) )
    
    
    
@app.put("/atualizarCliente/{id}", response_model=dict)
async def atualizar_cliente(
    id: str,
    data: dict,  
    current_user: dict = Depends(oauth2_scheme),  
):
    return atualizacao_dados_genericos(current_user,data,clientes.atualizar_dados, id)

    
@app.delete("/deletarCliente/{id}", response_model=dict)
async def deletar_arquivo(
    id: str,
    current_user: dict = Depends(oauth2_scheme)
):
    result = verifica_banco(current_user, clientes.deletar_cliente(id))

    return result


#### MAIN ######
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
