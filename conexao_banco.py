import yaml
from sqlalchemy import create_engine
import psycopg2

from properties import Properties  

class DatabaseConnector:
    def __init__(self, environment):
         self.properties = Properties(environment)

    def get_engine(self):
        db_host = self.properties.get("db")["host"]
        db_port = self.properties.get("db")["port"]
        db_database = self.properties.get("db")["database"]
        db_user = self.properties.get("db")["user"]
        db_password = self.properties.get("db")["password"]
        db_url = (
            f"postgresql://{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_database}"
        )
        engine = create_engine(db_url)
        return engine
    
    def get_connection(self):
        connection = psycopg2.connect(
            dbname=self.properties.get("db")["database"],
            user=self.properties.get("db")["user"],
            password=self.properties.get("db")["password"],
            host=self.properties.get("db")["host"],
            port=self.properties.get("db")["port"],
        )
        return connection
