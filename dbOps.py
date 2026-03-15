import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")

def query_db(query: str, return_df=True):

    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        f"Server={server};"
        f"Database={database};"
        "Trusted_Connection=yes;"
    )

    conn = pyodbc.connect(connection_string)

    df = pd.read_sql(query, conn)

    conn.close()

    if return_df:
        return df
    else:
        return df.to_string(index=False)