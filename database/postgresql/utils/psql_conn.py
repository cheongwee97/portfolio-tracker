import os
import psycopg2

from typing import Optional, Tuple, Any, Union, List

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

def query_table(query: str, values: Optional[Union[Tuple[Any, ...], list[Any]]] = None) -> List[Tuple[Any, ...]]:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values or ())
                return cur.fetchall()
    finally:
        conn.close()
