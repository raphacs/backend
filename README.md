comandos para funcionar o back:
set ENVIRONMENT=dev
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


# Backend

Este é o backend do projeto XYZ, desenvolvido em Python usando FastAPI e MySQL. O objetivo deste projeto é fornecer uma API para gerenciar e armazenar dados em um banco de dados MySQL.

## Requisitos

- Python 3.x
- FastAPI
- MySQL

## Instalação

1. Clone o repositório do projeto:

   ```shell
   git clone https://github.com/seu-usuario/backend.git
2. Acesse o diretorio do projeto:
   ```shell
   cd backend
   ```
3. Instale as dependências:
   ```shell
   pip install -r requirements.txt
   ```
4. Execute o script de configuração do projeto:
   ```shell
   set ENVIRONMENT=dev
   ```
5. Configure o arquivo de config:
   ```shell
   # Configurações de conexão com o banco de dados PostgreSQL
    db:
    host: 127.0.0.1
    port: 5432
    database: projeto
    user: postgres
    password: example

    token:
    host: http://localhost
    port: 8000
    user: raphael
    password: teste
    
    chaves: BilinuX01
   ```

6. Inicie o servidor:
   ```shell
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Estrutura do Projeto 
``` 

backend
├── arquivos
│   ├── arquivos.py
│── autenticacao
│   │── __init__.py 
│   │──jwt_utils.py
├── banco
│   │── __init__.py 
|   │── conexao_banco.py
├── clientes
│   │── __init__.py 
│   │── clientes.py
│── config
│   │── __init__.py 
│   │── config.py
|── modulos
│   │── __init__.py
│   │── modulos.py
|── planos
│   │── __init__.py
│   │── planos.py
├── relatorios
│   │── __init__.py
│   │── relatorios.py
|── usuarios
│   │── __init__.py
│   │── usuarios.py
│── main.py
│── requirements.txt
|── properties.py
|── utils.py

  
