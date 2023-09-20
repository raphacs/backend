import os
import jwt
from datetime import datetime, timedelta
from properties import Properties

class JWTUtils:
    def __init__(self, environment="dev"):
        self.properties = Properties(environment=environment)
        self.SECRET_KEY = self.properties.get("chaves")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 20

    def create_access_token(self, username: str, password: str):
        # Obtenha o valor do "basic auth" do arquivo YAML
        expected_username = self.properties.get("token")["user"]
        expected_password = self.properties.get("token")["password"]

        # Verifique se o "basic auth" fornecido corresponde ao armazenado no YAML
        if username == expected_username and password == expected_password:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode = {"exp": expire}
            encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
            
            remaining_minutes = int((expire - datetime.utcnow()).total_seconds() / 60)

            
            return {
                "access_token": encoded_jwt,
                "token_type": "bearer",
                "expires_in_minutes": int(remaining_minutes)
            }
        
        return None

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
