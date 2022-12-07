import pyodbc
from sqlalchemy import create_engine
import dotenv
import os
from urllib.parse import quote_plus
from sqlalchemy.engine import URL
from sqlalchemy import text

dotenv.load_dotenv(dotenv.find_dotenv())

Server = os.getenv('server')
usuario = os.getenv('UID')
tabela = os.getenv('Database')
password = os.getenv('PWD')

connection_url = URL.create(
    "mssql+pyodbc",
    username=f"{usuario}",
    password=f"{password}",
    host=f"{Server}",
    database=f"{tabela}",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "autocommit": "True",
    },
)




def get_engine():
    engine = create_engine(connection_url).execution_options(
        isolation_level="AUTOCOMMIT", future=True
    )
    return engine