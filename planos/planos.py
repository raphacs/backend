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
                query = """
                INSERT INTO plano (nome)
                VALUES (%(nome)s)
                """
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

        return {"message": "Plano ingerido com sucesso."}
    
    def inserir_dados_itens(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO plano_item (id_relatorio, id_plano)
                VALUES (%(id_relatorio)s, %(id_plano)s)
                """
                connection.execute(
                    query,
                    {
                        "id_relatorio": data["id_relatorio"],
                        "id_plano": data["id_plano"]

                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Item do plano ingerido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = "SELECT * FROM plano"  
            result = connection.execute(query)
            results = [dict(row) for row in result]
            return results
            
    def busca_plano(self, nome):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM plano WHERE nome = :nome")
            result = connection.execute(query, nome=nome)
            results = result.fetchone()  
            return dict(results) if results else None
        
    def busca_plano_item(self, id_plano):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM plano_item WHERE id_plano = :id_plano")
            result = connection.execute(query, id_plano=id_plano)
            results = result.fetchone()  
            return dict(results) if results else None
        
    def busca_plano_existe(self, nome):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM cliente WHERE nome = :nome")
            result = connection.execute(query, nome=nome)
            return result.fetchone() is not None