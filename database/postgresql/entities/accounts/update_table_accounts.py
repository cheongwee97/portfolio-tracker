from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from psycopg2 import errors

from database.postgresql.tables.accounts.obj.accounts import Account
from database.postgresql.utils.psql_conn import get_connection, execute

def create_account(account: Account) -> None:
    query_template = """
    INSERT INTO accounts (username, email, password_hash)
    VALUES (%s, %s, %s)
    """
    try:
        execute(query_template, (account.username, account.email, account.password_hash))
        return True
    except errors.UniqueViolation:
        # Handle username taken error
        print("Username already taken.")
        return False

def modify_account_username(account_id: str, new_username: str) -> bool:
    query_template = """
        UPDATE accounts
        SET username = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """
    try:
        execute(query_template, (new_username, account_id))
        return True
    except errors.UniqueViolation:
        # Handle username taken error
        print("Username already taken.")
        return False
    
def modify_account_email(account_id: str, new_email: str) -> bool:
    query_template = """
        UPDATE accounts
        SET email = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s    
    """
    try:
        execute(query_template, (new_email, account_id))
        return True
    except errors.UniqueViolation:
        print("Email already taken.")
        return False

def modify_password(account_id: str, new_password_hash: str) -> None:
    query_template = """
        UPDATE accounts
        SET password_hash = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """

    execute(query_template, (new_password_hash, account_id))


def delete_account(account_id: str) -> None:
    query_template = """
        DELETE FROM accounts
        WHERE id = %s
    """
    execute(query_template, (account_id,))

