from connect_database import dataframe_to_db_dev, dataframe_from_query_dev, insert_statement
from dotenv import load_dotenv

import os
import pandas as pd

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

def create_worker(list_workers: list):
    rows = []
    for TARGET_URL, prompt in list_workers:
        rows.append(
            {
                "target_url": TARGET_URL,
                "prompt": prompt,
            }
        )
    df = pd.DataFrame(rows)
    dataframe_to_db_dev(df, "workers", db=DB_NAME)

def find_workers(TARGET_URL: str, prompt: str):
    res = dataframe_from_query_dev(
        f"SELECT * from workers where (target_url = '{TARGET_URL}' and prompt = '{prompt}')"
    )
    if len(res.index):
        return res.to_dict("records")[0]
    else:
        return None

def describe_workers():
    res = dataframe_from_query_dev(f"SELECT target_url, prompt from workers")
    str_res = ""
    for row in res.to_dict("records"):
        str_res += f"TARGET_URL: {row['target_url']}\n\n PROMPT: {row['prompt']}"
    return str_res

def delete_worker(TARGET_URL: str, prompt: str):
    dataframe_from_query_dev(
        f"DELETE from workers where (target_url = '{TARGET_URL}' and prompt = '{prompt}')"
    )

def retrieve_previous_result(TARGET_URL: str, prompt: str):
    res = retrieve_history(TARGET_URL, prompt)
    if len(res):
        return res[-1]
    else:
        return None

def retrieve_history(TARGET_URL: str, prompt: str):
    return dataframe_from_query_dev(
        f"SELECT result from results where (target_url='{TARGET_URL}' and prompt='{prompt}')"
    ).to_dict("records")

def retrieve_comp_history(TARGET_URL: str, prompt: str):
    return dataframe_from_query_dev(
        f"SELECT result from comparisons where (target_url='{TARGET_URL}' and prompt='{prompt}')"
    ).to_dict("records")

def insert_result(TARGET_URL: str, prompt: str, result: str):
    insert_statement(query="INSERT INTO results (target_url, prompt, result) VALUES (?, ?, ?)", parameters=(TARGET_URL, prompt, result))

def insert_comparison(TARGET_URL: str, prompt: str, result: str):
    insert_statement(query="INSERT INTO comparisons (target_url, prompt, result) VALUES (?, ?, ?)", parameters=(TARGET_URL, prompt, result))

if __name__ == "__main__":
    TARGET_URL = os.getenv("TARGET_URL")
    EXTRACT_DATA_PROMPT = "Summarize in one paragraph the content of the page"
    
    print("These are the available workers")
    print(describe_workers())
    print(50*"*")
    print("This is the history of results in the db")
    print(retrieve_history(TARGET_URL, EXTRACT_DATA_PROMPT))
    print(50*"*")
