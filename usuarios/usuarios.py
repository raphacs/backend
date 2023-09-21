from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Usuarios:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO usuario (senha_hash, salt, usuario, admin, id_cliente)
                VALUES (%(senha_hash)s, %(salt)s, %(usuario)s, %(admin)s, %(id_cliente)s)
                """
                connection.execute(
                    query,
                    {
                        "senha_hash": data["senha_hash"],
                        "salt": data["salt"],
                        "usuario": data["usuario"],
                        "admin": data["admin"],
                        "id_cliente": data["id_cliente"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Usuario inserido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = "SELECT id, usuario, admin FROM usuario"  
            result = connection.execute(query)
            usuarios = [dict(row) for row in result]
            return usuarios
            
    def busca_usuario(self, nome_usuario):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM usuario WHERE usuario = :nome_usuario")
            result = connection.execute(query, nome_usuario=nome_usuario)
            usuario = result.fetchone()  
            return dict(usuario) if usuario else None
        
    def busca_usuario_existe(self, nome_usuario):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM usuario WHERE usuario = :nome_usuario")
            result = connection.execute(query, nome_usuario=nome_usuario)
            return result.fetchone() is not None