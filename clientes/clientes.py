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
    
    def busca_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, documento , status, id_plano FROM cliente")
            result = connection.execute(query)
            clientes = [{"id": row[0], "documento": row[1], "status": row[2], "id_plano": row[3]} for row in result.fetchall()]
            if clientes:
                return clientes
            else:
                raise HTTPException(status_code=500, detail=f"clientes nao encontrados")
            
    def busca_cliente(self, documento):
        with self.engine.connect() as connection:
            query = text("SELECT id, documento , status, id_plano  FROM cliente WHERE documento = :documento")
            result = connection.execute(query, {"documento": documento})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "documento": row[1], "status": row[2], "id_plano": row[3]}
            else:
                raise HTTPException(status_code=500, detail=f"cliente nao encontrado")
        
    def busca_cliente_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM cliente WHERE id = :id")
            result = connection.execute(query, {"id": id})
            cliente = result.fetchone()
            
            if cliente:
                return {"existe": True}
            else:
                return {"existe": False}