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
                existe = self.buscar_arquivo_existe(module_data["caminho_arquivo"], module_data["nome_arquivo"])
                print(existe)
                if not existe.get("existe"):
                    query = """
                    INSERT INTO arquivo (id,nome_arquivo, caminho_arquivo)
                    VALUES (:caminho_arquivo || '_' || :nome_arquivo, :nome_arquivo, :caminho_arquivo)
                    """
                    connection.execute(
                        text(query),
                        {
                            "nome_arquivo": module_data["nome_arquivo"],
                            "caminho_arquivo": module_data["caminho_arquivo"],
                        },
                    )
                    transaction.commit()
                else:
                    print('aqui' )
                    return { "message": "Arquivo já existe"}
            except Exception as e:
                print(str(e))
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o Arquivo: {str(e)}")

        return {"message": "Arquivo ingerido com sucesso."}

            
    def buscar_arquivo(self, cliente, nome_arquivo):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome_arquivo , caminho_arquivo  FROM arquivo WHERE nome_arquivo = :nome_arquivo and cliente = :cliente")
            result = connection.execute(query, {"nome_arquivo": nome_arquivo, "cliente":cliente})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "nome_arquivo": row[1], "caminho_arquivo": row[2]}
            else:
                raise HTTPException(status_code=500, detail=f"arquivo nao encontrado")
        
    def buscar_arquivo_existe(self, caminho_arquivo, nome_arquivo):
            with self.engine.connect() as connection:
                query = text("SELECT 1 FROM arquivo WHERE nome_arquivo = :nome_arquivo and caminho_arquivo = :caminho_arquivo")
                result = connection.execute(query, {"nome_arquivo": nome_arquivo, "caminho_arquivo":caminho_arquivo})
                arquivo = result.fetchone()
                
                if arquivo:
                    return {"existe": True}
                else:
                    return {"existe": False}
                
                
    def atualizar_dados(self, data, cliente_arquivo):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_arquivo_existe(cliente_arquivo["cliente"], cliente_arquivo["arquivo"])
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE arquivo
                    SET nome_arquivo = :nome_arquivo, caminho_arquivo = :caminho_arquivo, id = :caminho_arquivo || '_' || :nome_arquivo
                    WHERE nome_arquivo = :arquivo and 
                    caminho_arquivo = :cliente
                    """
                    connection.execute(
                        text(query),
                        {
                            "nome_arquivo": data["nome_arquivo"],
                            "caminho_arquivo": data["caminho_arquivo"],
                            "arquivo": cliente_arquivo["arquivo"],
                            "cliente": cliente_arquivo["cliente"]
                        },
                    )
                    transaction.commit()
                    return {"message": "Arquivo atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o arquivo: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Arquivo não existe")
            
    def deletar_arquivo(self, cliente_arquivo):
        with self.engine.connect() as connection:
            print(cliente_arquivo)
            existe = self.buscar_arquivo_existe(cliente_arquivo["cliente"], cliente_arquivo["arquivo"])
            
            if existe.get('existe'):
                query = text("DELETE FROM arquivo WHERE nome_arquivo = :nome_arquivo and caminho_arquivo = :caminho_arquivo")
                connection.execute(query, {"nome_arquivo": cliente_arquivo["arquivo"],  "caminho_arquivo": cliente_arquivo["cliente"]})
                return {"message": "Arquivo deletado com sucesso."}
            else:
                raise HTTPException(status_code=404, detail="Arquivo não encontrado, não é possível excluir.")