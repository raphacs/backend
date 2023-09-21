import requests

url = "http://localhost:8000/buscaPorUsuario"
params = {"usuario": "teste"}
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTUzMTAzNDN9.KQBokMD2sJBEwsKE5gwxLKhqbYrp3tcu8oQBEjhqL6Y"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Erro: {response.status_code}, Detalhe: {response.text}")
