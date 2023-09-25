from fastapi import HTTPException
from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Planos:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = text("""
                INSERT INTO plano (nome)
                VALUES (:nome)
                """)
                connection.execute(
                    query,
                    {
                        "nome": data["nome"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Plano inserido com sucesso."}


    
    def inserir_dados_itens(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO plano_item (id_relatorio, id_plano)
                VALUES (:id_relatorio, :id_plano)
                """
                connection.execute(
                    text(query),
                    {
                        "id_relatorio": data["id_relatorio"],
                        "id_plano": data["id_plano"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Item do plano ingerido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome FROM plano")
            result = connection.execute(query)
            planos = [{"id": row[0], "nome": row[1]} for row in result.fetchall()]
            if planos:
                return planos
            else:
                raise HTTPException(status_code=500, detail=f"planos nao encontrados")
            
            
    def busca_plano(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome FROM plano WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "nome": row[1]}
            else:
                raise HTTPException(status_code=500, detail=f"plano nao encontrado")
            
    def busca_plano_item(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT id, id_relatorio, id_plano FROM plano_item WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "id_relatorio": row[1], "id_plano": row[2]}
            else:
                raise HTTPException(status_code=500, detail=f"item do plano nao encontrado")
        
        
        
    def busca_plano_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM plano WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"existe": True}
            else:
                return {"existe": False}