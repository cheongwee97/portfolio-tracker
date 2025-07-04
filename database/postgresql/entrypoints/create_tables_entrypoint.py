import glob
from typing import List
from database.postgresql.utils.psql_conn import execute

def get_all_create_table_path() -> List[str]:
    files = glob.glob("database/postgresql/tables/**/create_table_*.sql", recursive=True)
    return files

def read_sql_file(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()
    
def execute_create_table(create_table_sql: str) -> None:
    execute(create_table_sql, ())

def main():
    files = get_all_create_table_path()
    for fp in files:
        create_table_sql = read_sql_file(fp)
        execute_create_table(create_table_sql=create_table_sql)

if __name__ == "__main__":
    main()