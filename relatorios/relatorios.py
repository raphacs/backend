from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Relatorios:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, module_data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO relatorio (descricao, ordem, status, id_report,id_workspace, id_dataset, role, id_arquivo, id_modulo)
                VALUES (%(descricao)s, %(ordem)s, %(status)s, %(id_report)s, %(id_workspace)s, %(id_dataset)s, %(role)s, %(id_arquivo)s, %(id_modulo)s)
                """
                connection.execute(
                    query,
                    {
                        "descricao": module_data["descricao"],
                        "ordem": module_data["ordem"],
                        "status": module_data["status"],
                        "id_report": module_data["id_report"],
                        "id_workspace": module_data["id_workspace"],
                        "id_dataset": module_data["id_dataset"],
                        "role": module_data["role"],
                        "id_arquivo": module_data["id_arquivo"],
                        "id_modulo": module_data["id_modulo"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Relatorio ingerido com sucesso."}
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = "SELECT * FROM relatorio"  
            result = connection.execute(query)
            results = [dict(row) for row in result]
            return results
            
    def busca_relatorio(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM relatorio WHERE id = :id")
            result = connection.execute(query, id=id)
            results = result.fetchone()  
            return dict(results) if results else None
        
    def busca_relatorio_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM relatorio WHERE id = :id")
            result = connection.execute(query, id=id)
            return result.fetchone() is not None