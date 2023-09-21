from banco.conexao_banco import DatabaseConnector
from sqlalchemy import create_engine, text

class Arquivos:
    def __init__(self, environment):
        self.db_connector = DatabaseConnector(environment)
        self.engine = self.db_connector.get_engine()

    def inserir_dados(self, module_data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO arquivo (nome_arquivo, caminho_arquivo)
                VALUES (%(nome_arquivo)s, %(caminho_arquivo)s)
                """
                connection.execute(
                    query,
                    {
                        "nome_arquivo": module_data["nome_arquivo"],
                        "caminho_arquivo": module_data["caminho_arquivo"],
                        
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        return {"message": "Arquivo ingerido com sucesso."}

            
    def busca_arquivo(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT * FROM arquivo WHERE id = :id")
            result = connection.execute(query, id=id)
            results = result.fetchone()  
            return dict(results) if results else None
        
