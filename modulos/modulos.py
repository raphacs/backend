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
        
    def buscar_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, descricao, ordem, status, id_arquivo FROM modulo")
            result = connection.execute(query)
            modulos = [{"id": row[0], "descricao": row[1], "ordem": row[2], "status": row[3], "id_arquivo": row[4]} for row in result.fetchall()]
            if modulos:
                return modulos
            else:
                raise HTTPException(status_code=500, detail=f"Modulos nao encontrados")
            
    def buscar_modulo(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT id, descricao, ordem, status, id_arquivo  FROM modulo WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "descricao": row[1], "ordem": row[2], "status": row[3], "id_arquivo": row[4]}
            else:
                raise HTTPException(status_code=500, detail=f"Modulo nao encontrado")
        
    def buscar_modulo_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM modulo WHERE id = :id")
            result = connection.execute(query, {"id": id})
            modulo = result.fetchone()
            
            if modulo:
                return {"existe": True}
            else:
                return {"existe": False}
            
    def atualizar_dados(self, data, modulo):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_modulo_existe(modulo)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE modulo
                    SET descricao = :descricao, ordem = :ordem, id_arquivo = :id_arquivo
                    WHERE id = :id
                    """
                    connection.execute(
                        text(query),
                        {
                            "descricao": data["descricao"],
                            "ordem": data["ordem"],
                            "id_arquivo": data["id_arquivo"],
                            "id": modulo
                        },
                    )
                    transaction.commit()
                    return {"message": "Modulo atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o modulo: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Modulo não existe")



    def deletar_modulo(self, modulo):
        
            with self.engine.connect() as connection:
                
                existe = self.buscar_modulo_existe(modulo)
                
                if existe.get('existe'):
                    query = text("DELETE FROM modulo WHERE id = :id")
                    connection.execute(query, {"id": modulo})
                    return {"message": "Modulo deletado com sucesso."}
                else:
                    raise HTTPException(status_code=404, detail="Modulo não encontrado, não é possível excluir.")
        