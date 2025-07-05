import os
from typing import List

from database.postgresql.utils.psql_conn import execute


def create_required_extensions():
    print("📦 Creating required extensions...")
    execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def get_ordered_sql_paths() -> List[str]:
    return [
        # Tables
        "database/postgresql/entities/accounts/tables/create_table_accounts.sql",
        "database/postgresql/entities/portfolio/tables/create_table_portfolios.sql",
        "database/postgresql/entities/portfolio/tables/create_table_portfolios_holdings.sql",

        # Functions
        "database/postgresql/entities/portfolio/functions/create_function_notify_ticker_change.sql",

        # Triggers
        "database/postgresql/entities/portfolio/triggers/create_trigger_ticker_change.sql"
    ]


def read_sql_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    print("🚀 Starting PostgreSQL SQL bootstrap...")
    create_required_extensions()

    for path in get_ordered_sql_paths():
        print(f"▶ Executing {path}")
        sql = read_sql_file(path)
        execute(sql)

    print("\n✅ All SQL setup complete!")


if __name__ == "__main__":
    main()