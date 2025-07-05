import os
import psycopg2

from dotenv import load_dotenv
from typing import Optional, Tuple, Any, Union, List

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )


def execute(query: str, values: Optional[Union[Tuple[Any, ...], list[Any]]] = None) -> None:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values or ())
    finally:
        conn.close()

def query_table(
    query: str,
    values: Optional[Union[Tuple[Any, ...], List[Any]]] = None,
    fetch: str = 'all',
    many_size: int = 10
) -> Union[List[Tuple[Any, ...]], Tuple[Any, ...], None]:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values or ())
                
                if fetch == 'all':
                    return cur.fetchall()
                elif fetch == 'one':
                    return cur.fetchone()
                elif fetch == 'many':
                    return cur.fetchmany(many_size)
                else:
                    raise ValueError(f"Unknown fetch option: {fetch}")
    finally:
        conn.close()

conn = get_connection()