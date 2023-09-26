from fastapi import HTTPException
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
                query = text("""
                INSERT INTO relatorio (descricao, ordem, status, id_report, id_workspace, id_dataset, role, id_arquivo, id_modulo)
                VALUES (:descricao, :ordem, :status, :id_report, :id_workspace, :id_dataset, :role, :id_arquivo, :id_modulo)
                """)
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
                raise HTTPException(status_code=500, detail=f"Erro ao inserir o relatório: {str(e)}")

        return {"message": "Relatório ingerido com sucesso."}

    
    def buscar_todos(self):
        with self.engine.connect() as connection:
            query = text("SELECT id, descricao, ordem , status, id_report, id_workspace, id_dataset, role, id_arquivo, id_modulo FROM relatorio")
            result = connection.execute(query)
            relatorios = [{"id": row[0], "descricao": row[1], "ordem": row[2], "status": row[3], "id_report": row[4], "id_workspace": row[5], "id_dataset": row[6], "role": row[7], "id_arquivo": row[8], "id_modulo": row[9]} for row in result.fetchall()]
            if relatorios:
                return relatorios
            else:
                raise HTTPException(status_code=500, detail=f"relatorios nao encontrados")
            
            
    def buscar_relatorio(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT id, descricao, ordem , status, id_report, id_workspace, id_dataset, role, id_arquivo, id_modulo FROM relatorio WHERE id = :id")
            result = connection.execute(query, {"id": id})
            row = result.fetchone()
            
            if row:
                return {"id": row[0], "descricao": row[1], "ordem": row[2], "status": row[3], "id_report": row[4], "id_workspace": row[5], "id_dataset": row[6], "role": row[7], "id_arquivo": row[8], "id_modulo": row[9]}
            else:
                raise HTTPException(status_code=500, detail=f"relatorio nao encontrado")
        
        
    def buscar_relatorio_existe(self, id):
        with self.engine.connect() as connection:
            query = text("SELECT 1 FROM relatorio WHERE id = :id")
            result = connection.execute(query, {"id": id})
            relatorio = result.fetchone()
            
            if relatorio:
                return {"existe": True}
            else:
                return {"existe": False}
            
            
    def atualizar_dados(self, module_data, relatorio):
        with self.engine.connect() as connection:
            transaction = connection.begin()
            existe = self.buscar_relatorio_existe(relatorio)
            if existe.get("existe"):
                try:
                    query = """
                    UPDATE relatorio
                    SET descricao = :descricao, ordem = :ordem, status = :status, id_report = :id_report, id_workspace = :id_workspace, id_dataset = :id_dataset, role = :role, id_arquivo = :id_arquivo, id_modulo = :id_modulo
                    WHERE id = :idRelatorio
                    """
                    connection.execute(
                        text(query),
                        {
                            "descricao": module_data["descricao"],
                            "ordem": module_data["ordem"],
                            "status": module_data["status"],
                            "id_report": module_data["id_report"],
                            "id_workspace": module_data["id_workspace"],
                            "id_dataset": module_data["id_dataset"],
                            "role": module_data["role"],
                            "id_arquivo": module_data["id_arquivo"],
                            "id_modulo": module_data["id_modulo"],
                            "idRelatorio": relatorio
                        },
                    )
                    transaction.commit()
                    return {"message": "Relatorio atualizado com sucesso."}
                except Exception as e:
                    transaction.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao atualizar o relatorio: {str(e)}")

                
            else:
                raise HTTPException(status_code=500, detail=f"Relatorio não existe")
            
            
            
    def deletar_usuario(self, idRelatorio):
        with self.engine.connect() as connection:
            
            relatorio_existente = self.buscar_relatorio_existe(idRelatorio)
            
            if relatorio_existente.get('existe'):
                query = text("DELETE FROM relatorio WHERE id = :idRelatorio")
                connection.execute(query, {"idRelatorio": idRelatorio})
                return {"message": "Relatorio deletado com sucesso."}
            else:
                raise HTTPException(status_code=404, detail="Relatorio não encontrado, não é possível excluir.")