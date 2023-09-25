from fastapi import HTTPException
from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Modulos:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, module_data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO modulo (descricao, ordem, status, id_arquivo)
                VALUES (:descricao, :ordem, :status, :id_arquivo)
                """
                connection.execute(
                    text(query),
                    {
                        "descricao": module_data["descricao"],
                        "ordem": module_data["ordem"],
                        "status": module_data["status"],
                        "id_arquivo": module_data["id_arquivo"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Módulo ingerido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = "SELECT * FROM modulo"  
            result = connection.execute(query)
            results = [dict(row) for row in result]
            return results
            
    def busca_modulo(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM modulo WHERE id = :id")
            result = connection.execute(query, id=id)
            results = result.fetchone()  
            return dict(results) if results else None
        
    def busca_modulo_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM modulo WHERE id = :id")
            result = connection.execute(query, id=id)
            return result.fetchone() is not None