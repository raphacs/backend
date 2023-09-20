from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Ingestor:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, module_data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO modulos_bi (descricao, ordem, status, id_arquivo)
                VALUES (%(descricao)s, %(ordem)s, %(status)s, %(id_arquivo)s)
                """
                connection.execute(
                    query,
                    {
                        "descricao": module_data["descricao"],
                        "ordem": module_data["ordem"],
                        "status": module_data["status"],
                        "id_arquivo": module_data["id_arquivo"],
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Módulo ingerido com sucesso."}
