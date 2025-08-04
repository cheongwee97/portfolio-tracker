import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class PostgresClient:
    def __init__(self, host=None, dbname=None, dbuser=None, dbpass=None, dbport=None):
        self.host = os.getenv("POSTGRES_HOST")
        self.dbname = os.getenv('POSTGRES_DB')
        self.dbuser = os.getenv('POSTGRES_USER')
        self.dbpass = os.getenv('POSTGRES_PASSWORD')
        self.dbport = os.getenv('POSTGRES_PORT')
        self.connection_params = {
            'host': self.host,
            'database': self.dbname,
            'user': self.dbuser,
            'password': self.dbpass,
            'port': self.dbport
        }
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host, 
            dbname=self.dbname,
            user=self.dbuser,
            password=self.dbpass,
            port=self.dbport
            )
        
        return self.conn
    
    def execute_query(self, query, params=None, fetch=None, fetch_size=10):
        if not self.conn:
            raise Exception("Not connected to database")
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                result = None
                if fetch == 'all':
                    result = cur.fetchall()
                elif fetch == 'one':
                    result = cur.fetchone()
                elif fetch == 'many':
                    result = cur.fetchmany(fetch_size)

                self.conn.commit()

                return result
        except Exception as e:
            self.conn.rollback()
            print(f"Error: {e}")
            return None