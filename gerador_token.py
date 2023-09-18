import jwt
import yaml

def generate_token(environment="dev"):
    # Carregue as configurações do arquivo YAML
    config_file_path = f"config-{environment}.yaml"
    with open(config_file_path, "r") as config_file:
        config_data = yaml.safe_load(config_file)
        token_config = config_data["token"]

    # Crie o payload do token com base nas configurações
    payload = {
        "host": token_config["host"],
        "port": token_config["port"],
        "user": token_config["user"],
        # Não inclua a senha no payload do token por motivos de segurança
    }

    # Gere o token com base no payload
    secret_key = "sua_chave_secreta"  # Substitua pela sua chave secreta
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

if __name__ == "__main__":
    # Chame a função generate_token com o ambiente desejado (por exemplo, "dev" ou "prod")
    ambiente = "dev"
    token_gerado = generate_token(environment=ambiente)
    print(f"Token gerado para ambiente '{ambiente}':")
    print(token_gerado)
