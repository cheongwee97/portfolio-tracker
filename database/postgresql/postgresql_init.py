import os
import sys
from typing import List

from database.postgresql.conn.psql_client import PostgresClient


def read_sql_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def get_create_extensions_path() -> List[str]:
    return [
        "database/postgresql/extensions/create_extensions.sql"
    ]

def get_create_tables_path() -> List[str]:
    return [
        "database/postgresql/tables/create_table_sql/user_tables/create_account_table.sql",
        "database/postgresql/tables/create_table_sql/user_tables/create_portfolio_table.sql",
        "database/postgresql/tables/create_table_sql/user_tables/create_transaction_table.sql",
        "database/postgresql/tables/create_table_sql/asset_tables/create_ticker_metadata_table.sql",
        "database/postgresql/tables/create_table_sql/asset_tables/create_ticker_prices_table.sql",
        "database/postgresql/tables/create_table_sql/asset_tables/create_ticker_daily_table.sql"
    ]

def get_create_mv_path() -> List[str]:
    return [
        "database/postgresql/materialised_views/create_current_holdings_mv.sql",
        "database/postgresql/materialised_views/create_portfolio_valuations_mv.sql",
        "database/postgresql/materialised_views/create_portfolio_summary_mv.sql",
        "database/postgresql/materialised_views/create_daily_portfolio_snapshot_mv.sql",
    ]

def get_all_paths() -> List[str]:
    all_paths = get_create_extensions_path() + get_create_tables_path() + get_create_mv_path()
    return all_paths



def main():
    # SQL files in order of execution
    sql_files = get_all_paths()

    # Create a PostgresClient instance
    client = PostgresClient()

    try:
        # Connect to the database
        client.connect()

        # Execute each SQL file
        for sql_file in sql_files:
            # Construct the absolute path to the SQL file
            abs_sql_file_path = os.path.join(sql_file)
            print(f"Executing {abs_sql_file_path}...")
            query = read_sql_file(abs_sql_file_path)
            client.execute_query(query)
            print(f"Successfully executed {sql_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if client.conn:
            client.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
