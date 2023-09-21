from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Clientes:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, module_data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO cliente (documento,  status, id_plano )
                VALUES (%(documento)s,  %(status)s,  %(id_plano)s)
                """
                connection.execute(
                    query,
                    {
                        "documento": module_data["documento"],
                        "status": module_data["status"],
                        "id_plano": module_data["id_plano"]
                        
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Cliente ingerido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = "SELECT * FROM cliente"  
            result = connection.execute(query)
            results = [dict(row) for row in result]
            return results
            
    def busca_cliente(self, documento):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM cliente WHERE documento = :documento")
            result = connection.execute(query, documento=documento)
            results = result.fetchone()  
            return dict(results) if results else None
        
    def busca_cliente_existe(self, documento):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM cliente WHERE documento = :documento")
            result = connection.execute(query, documento=documento)
            return result.fetchone() is not None