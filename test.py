import httpx

# Dados que você deseja ingerir
data_to_ingest = {
    "module_name": "Exemplo de Módulo",
    "descricao": "Descrição do módulo de exemplo",
    "ordem": 1,
    "status": True,
    "id_arquivo": 1
}

# Token de autenticação JWT (substitua pelo seu token válido)
jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJob3N0IjoiaHR0cDovL2xvY2FsaG9zdCIsInBvcnQiOjgwMDAsInVzZXIiOiJyYXBoYWVsIn0.iicKY0Le2B7l8ZdhFv3_wLC5IDoh0WbK7wbq274FeO3"

# URL base do servidor FastAPI
base_url = "http://localhost:8000"  # Substitua pela URL correta

# Headers com o token JWT
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json",
}

# Realize a requisição para a rota /ingerirModulo
response = httpx.post(
    f"{base_url}/ingerirModulo",
    json=data_to_ingest,
    headers=headers,
)

# Verifique a resposta
if response.status_code == 200:
    print("Módulo ingerido com sucesso!")
else:
    try:
        error_detail = response.json().get("detail", "Erro desconhecido")
        if isinstance(error_detail, dict):
            # Se 'detail' é um dicionário, tente obter 'msg' dele
            error_detail = error_detail.get("msg", "Erro desconhecido")
        print(f"Erro ao ingerir o módulo: {error_detail}")
    except Exception as e:
        print(f"Erro ao analisar a resposta: {e}")
