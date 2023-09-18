import os
import jwt
from datetime import datetime, timedelta

# Chave secreta para assinar o token (mantenha esta chave em segurança)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

# Algoritmo de criptografia para assinar o token
ALGORITHM = "HS256"

# Tempo de validade do token (por exemplo, 1 hora)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
