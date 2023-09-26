from fastapi import HTTPException
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
                INSERT INTO cliente (documento, status, id_plano)
                VALUES (:documento, :status, :id_plano)
                """
                connection.execute(
                    text(query),
                    {
                        "documento": module_data["documento"],
                        "status": module_data["status"],
                        "id_plano": module_data["id_plano"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Cliente ingerido com sucesso."}
    
    def buscar_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, documento , status, id_plano FROM cliente")
            result = connection.execute(query)
            clientes = [{"id": row[0], "documento": row[1], "status": row[2], "id_plano": row[3]} for row in result.fetchall()]
            if clientes:
                return clientes
            else:
                raise HTTPException(status_code=500, detail=f"clientes nao encontrados")
            
    def buscar_cliente(self, documento):
        with self.engine.connect() as connection:
            query = text("SELECT id, documento , status, id_plano  FROM cliente WHERE documento = :documento")
            result = connection.execute(query, {"documento": documento})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "documento": row[1], "status": row[2], "id_plano": row[3]}
            else:
                raise HTTPException(status_code=500, detail=f"cliente nao encontrado")
        
    def buscar_cliente_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM cliente WHERE id = :id")
            result = connection.execute(query, {"id": id})
            cliente = result.fetchone()
            
            if cliente:
                return {"existe": True}
            else:
                return {"existe": False}
            
    def atualizar_dados(self, data, cliente):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_cliente_existe(cliente)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE cliente
                    SET documento = :documento, status = :status, id_plano = :id_plano
                    WHERE id = :id
                    """
                    connection.execute(
                        text(query),
                        {
                            "documento": data["documento"],
                            "status": data["status"],
                            "id_plano": data["id_plano"],
                            "id": cliente
                        },
                    )
                    transaction.commit()
                    return {"message": "Cliente atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o cliente: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Cliente não existe")



    def deletar_cliente(self, cliente):
        try:
            with self.engine.connect() as connection:
                
                existe = self.buscar_cliente_existe(cliente)
                
                if existe.get('existe'):
                    query = text("DELETE FROM cliente WHERE id = :id")
                    connection.execute(query, {"id": cliente})
                    return {"message": "Cliente deletado com sucesso."}
                else:
                    raise HTTPException(status_code=404, detail="Cliente não encontrado, não é possível excluir.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar o cliente: {str(e)}")