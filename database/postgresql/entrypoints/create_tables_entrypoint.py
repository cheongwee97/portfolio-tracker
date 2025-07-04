from typing import List
from database.postgresql.utils.psql_conn import execute

def create_required_extensions():
    uuid_extension = "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"";
    execute(uuid_extension)

def get_all_create_table_path() -> List[str]:
    ordered_files = [
        "database/postgresql/tables/accounts/create_table_accounts.sql",
        "database/postgresql/tables/portfolio/create_table_portfolios_holdings.sql",
        "database/postgresql/tables/portfolio/create_table_portfolios.sql"
    ]
    return ordered_files

def read_sql_file(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()
    
def execute_create_table(create_table_sql: str) -> None:
    execute(create_table_sql, ())

def main():
    create_required_extensions()

    ordered_files = get_all_create_table_path()
    for fp in ordered_files:
        create_table_sql = read_sql_file(fp)
        execute_create_table(create_table_sql=create_table_sql)

if __name__ == "__main__":
    main()