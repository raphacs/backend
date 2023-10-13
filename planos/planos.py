from fastapi import HTTPException
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
                query = text("""
                INSERT INTO plano (nome)
                VALUES (:nome)
                """)
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

        return {"message": "Plano inserido com sucesso."}


    
    def inserir_dados_itens(self, data):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = """
                INSERT INTO plano_item (id_relatorio, id_plano)
                VALUES (:id_relatorio, :id_plano)
                """
                connection.execute(
                    text(query),
                    {
                        "id_relatorio": data["id_relatorio"],
                        "id_plano": data["id_plano"]
                    },
                )
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Item do plano ingerido com sucesso."}
    
    def buscar_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome FROM plano")
            result = connection.execute(query)
            planos = [{"id": row[0], "nome": row[1]} for row in result.fetchall()]
            if planos:
                return planos
            else:
                raise HTTPException(status_code=500, detail=f"planos nao encontrados")
            
            
    def buscar_plano(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT id, nome FROM plano WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "nome": row[1]}
            else:
                raise HTTPException(status_code=500, detail=f"plano nao encontrado")
            
    def buscar_plano_itens(self, id_plano):
        with self.engine.connect() as connection:
            query = text("SELECT id, id_relatorio, id_plano FROM plano_item where id_plano = :id_plano")
            result = connection.execute(query, {"id_plano":id_plano})
            planos = [{"id": row[0], "id_relatorio": row[1], "id_plano": row[2]} for row in result.fetchall()]
            if planos:
                return planos
            else:
                raise HTTPException(status_code=500, detail=f"itens do plano nao encontrados")
            
    def buscar_plano_itens_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM plano_item where id = :id")
            result = connection.execute(query, {"id":id})
            row = result.fetchone()
            if row:
                return {"existe": True}
            else:
                return {"existe": False}
        
        
        
    def buscar_plano_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM plano WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"existe": True}
            else:
                return {"existe": False}
            
            
            
    def atualizar_dados(self, data, plano):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_plano_existe(plano)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE plano
                    SET nome = :nome
                    WHERE id = :id
                    """
                    connection.execute(
                        text(query),
                        {
                            "nome": data["nome"],
                            "id": plano
                        },
                    )
                    transaction.commit()
                    return {"message": "Plano atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o plano: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Plano não existe")

    def atualizar_item_plano(self, data, id):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_plano_itens_existe(id)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE plano_item
                    SET id_relatorio = :id_relatorio, id_plano = :id_plano
                    WHERE id = :id
                    """
                    connection.execute(
                        text(query),
                        {
                            "id_relatorio": data["id_relatorio"],
                            "id_plano": data["id_plano"],
                            "id": id
                        },
                    )
                    transaction.commit()
                    return {"message": "Item do Plano atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item do Plano: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"item do Plano não existe")

    def deletar_plano(self, plano):
        
            with self.engine.connect() as connection:
                
                existe = self.buscar_plano_existe(plano)
                
                if existe.get('existe'):
                    query = text("DELETE FROM plano WHERE id = :id")
                    connection.execute(query, {"id": plano})
                    return {"message": "Plano deletado com sucesso."}
                else:
                    raise HTTPException(status_code=404, detail="Plano não encontrado, não é possível excluir.")
    
    def deletar_plano_item(self, plano):
            with self.engine.connect() as connection:
                
                existe = self.buscar_plano_itens_existe(plano)
                print(existe)
                if existe.get('existe'):
                    query = text("DELETE FROM plano_item WHERE id = :id")
                    connection.execute(query, {"id": plano})
                    return {"message": "Item Plano deletado com sucesso."}
                else:
                    raise HTTPException(status_code=404, detail="Item Plano não encontrado, não é possível excluir.")