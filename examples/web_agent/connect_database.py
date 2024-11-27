from dotenv import load_dotenv

import pandas as pd
import sqlite3
import os

load_dotenv()


DB_NAME = os.getenv("DB_NAME")


def connect_dev(db=DB_NAME):
    return sqlite3.connect(f"{db}")


def dataframe_from_query_dev(query: str, db=DB_NAME):
    engine = connect_dev(db=db)
    return pd.read_sql(query, con=engine)


def dataframe_to_db_dev(df: pd.DataFrame, table_name: str, db=DB_NAME):
    engine = connect_dev(db=db)
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

def insert_statement(query, parameters):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()

def insert_tables(query):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

sql_statements = ["""
CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY, 
    target_url text NOT NULL, 
    prompt text NOT NULL
);
""",
"""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY, 
    target_url text NOT NULL, 
    prompt text NOT NULL,
    result text NOT NULL
);
""",
"""
CREATE TABLE IF NOT EXISTS comparisons (
    id INTEGER PRIMARY KEY, 
    target_url text NOT NULL, 
    prompt text NOT NULL,
    result text NOT NULL
);
""",
]

if __name__ == "__main__":
    for statement in sql_statements:
        insert_tables(statement)
