from fastapi import HTTPException
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
                VALUES (:nome_arquivo, :caminho_arquivo)
                """
                connection.execute(
                    text(query),
                    {
                        "nome_arquivo": module_data["nome_arquivo"],
                        "caminho_arquivo": module_data["caminho_arquivo"],
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Arquivo ingerido com sucesso."}

            
    def busca_arquivo(self, nome_arquivo):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome_arquivo , caminho_arquivo  FROM arquivo WHERE nome_arquivo = :nome_arquivo")
            result = connection.execute(query, {"nome_arquivo": nome_arquivo})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "nome_arquivo": row[1], "caminho_arquivo": row[2]}
            else:
                raise HTTPException(status_code=500, detail=f"arquivo nao encontrado")
        
    def busca_arquivo_existe(self, nome_arquivo):
            with self.engine.connect() as connection:
                query = text("SELECT 1 FROM arquivo WHERE nome_arquivo = :nome_arquivo")
                result = connection.execute(query, {"nome_arquivo": nome_arquivo})
                arquivo = result.fetchone()
                
                if arquivo:
                    return {"existe": True}
                else:
                    return {"existe": False}