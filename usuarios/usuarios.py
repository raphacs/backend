from fastapi import HTTPException
from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text
from utils import criar_salt, criar_hash_senha

class Usuarios:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            
            salt = criar_salt()
            
            try:
                query = """
                INSERT INTO usuario (senha_hash, salt, usuario, admin, id_cliente)
                VALUES (:senha_hash, :salt, :usuario, :admin, :id_cliente)
                """
                connection.execute(
                    text(query),
                    {
                        "senha_hash": (criar_hash_senha(data["senha_hash"],salt).decode('utf-8')),
                        "salt": salt.decode('utf-8'),
                        "usuario": (data["usuario"].upper()),
                        "admin": data["admin"],
                        "id_cliente": data["id_cliente"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Usuário inserido com sucesso."}
    
    def buscar_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, usuario, admin FROM usuario")
            result = connection.execute(query)
            usuarios = [{"id": row[0], "usuario": row[1], "admin": row[2]} for row in result.fetchall()]
            if usuarios:
                return usuarios
            else:
                raise HTTPException(status_code=500, detail=f"usuarios nao encontrados")

            
    def buscar_usuario(self, nome_usuario):
        with self.engine.connect() as connection:
            query = text("SELECT id, usuario, admin, senha_hash, salt, id_cliente FROM usuario WHERE usuario = :nome_usuario")
            result = connection.execute(query, {"nome_usuario": nome_usuario})
            usuario = result.fetchone()
            if usuario:
                return {"id": usuario[0], "usuario": usuario[1], "admin": usuario[2], "senha_hash": usuario[3], "salt": usuario[4], "id_cliente": usuario[5]}
            else:
                raise HTTPException(status_code=500, detail=f"usuario nao encontrado")


        
    def buscar_usuario_existe(self, nome_usuario):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM usuario WHERE usuario = :nome_usuario")
            result = connection.execute(query, {"nome_usuario": nome_usuario})
            usuario = result.fetchone()
            
            if usuario:
                return {"existe": True}
            else:
                return {"existe": False}
            
            
    def atualizar_dados(self, data, usuario):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_usuario_existe(usuario)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE usuario
                    SET senha_hash = :senha_hash, admin = :admin, id_cliente = :id_cliente, usuario = :usuario
                    WHERE usuario = :usuariobuscar
                    """
                    connection.execute(
                        text(query),
                        {
                            "senha_hash": data["senha_hash"],
                            "admin": data["admin"],
                            "id_cliente": data["id_cliente"],
                            "usuario": data["usuario"],
                            "usuariobuscar": usuario
                        },
                    )
                    transaction.commit()
                    return {"message": "Usuário atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o usuário: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Usuario não existe")



    def deletar_usuario(self, nome_usuario):
            with self.engine.connect() as connection:
                
                usuario_existente = self.buscar_usuario_existe(nome_usuario)
                
                if usuario_existente.get('existe'):
                    query = text("DELETE FROM usuario WHERE usuario = :nome_usuario")
                    connection.execute(query, {"nome_usuario": nome_usuario})
                    return {"message": "Usuário deletado com sucesso."}
                else:
                    raise HTTPException(status_code=404, detail="Usuário não encontrado, não é possível excluir.")