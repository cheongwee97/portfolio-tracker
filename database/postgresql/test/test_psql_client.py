import unittest
import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from database.postgresql.conn.psql_client import PostgresClient

# Load environment variables from .env file
load_dotenv()

class TestDatabaseConnection(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = PostgresClient()
        self.client.connect()
    
    def test_connection_parameters_exist(self):
        """Test that all required connection parameters are available."""
        print("Testing if all required connection parameters are available")
        required_params = ['host', 'database', 'user', 'password', 'port']
        for param in required_params:
            with self.subTest(param=param):
                value = self.client.connection_params.get(param)
                self.assertIsNotNone(value, f"{param} is missing in connection_params")
                self.assertNotEqual(value, '', f"{param} is empty in connection_params")
    
    def test_database_connection(self):
        """Test database connection."""
        conn = self.client.connect()
        try:
            self.assertIsNotNone(conn)
            self.assertEqual(conn.closed, 0)  # 0 means connection is open
            print(f"Successfully connected to {self.client.connection_params['database']} on {self.client.connection_params['host']}")
        except OperationalError as e:
            self.fail(f"Failed to connect to database: {e}")
        except Exception as e:
            self.fail(f"Unexpected error during connection: {e}")
        finally:
            if conn and not conn.closed:
                conn.close()

    @patch("database.postgresql.conn.psql_client.psycopg2.connect")
    def test_execute_fetch_all(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("Alice",), ("Bob",)]

        client = PostgresClient("localhost", "testdb", "user", "pass")
        client.connect()

        result = client.execute_query("SELECT * FROM test;", fetch='all')

        mock_cursor.execute.assert_called_once_with("SELECT * FROM test;", None)
        mock_cursor.fetchall.assert_called_once()
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, [("Alice",), ("Bob",)])

    @patch("database.postgresql.conn.psql_client.psycopg2.connect")
    def test_execute_fetch_one(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("Alice",)

        client = PostgresClient("localhost", "testdb", "user", "pass")
        client.connect()

        result = client.execute_query("SELECT * FROM test;", fetch='one')

        mock_cursor.execute.assert_called_once_with("SELECT * FROM test;", None)
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, ("Alice",))

    @patch("database.postgresql.conn.psql_client.psycopg2.connect")
    def test_execute_fetch_many(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock fetchmany return value with 3 rows
        mock_cursor.fetchmany.return_value = [("Alice",), ("Bob",), ("Charlie",)]

        client = PostgresClient("localhost", "testdb", "user", "pass")
        client.connect()

        result = client.execute_query("SELECT * FROM test;", fetch='many', fetch_size=3)

        mock_cursor.execute.assert_called_once_with("SELECT * FROM test;", None)
        mock_cursor.fetchmany.assert_called_once_with(3)
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, [("Alice",), ("Bob",), ("Charlie",)])
    
    @patch("database.postgresql.conn.psql_client.psycopg2.connect")
    def test_execute_create_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        client = PostgresClient("localhost", "testdb", "user", "pass")
        client.connect()

        create_table_sql = """
            CREATE TABLE test (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """

        result = client.execute_query(create_table_sql)

        # Assert execute called with the right query and no params
        mock_cursor.execute.assert_called_once_with(create_table_sql, None)

        # Assert commit was called
        mock_conn.commit.assert_called_once()

        # Since no fetching, result should be None
        assert result is None

        # Make sure no fetch methods were called
        mock_cursor.fetchone.assert_not_called()
        mock_cursor.fetchall.assert_not_called()
        mock_cursor.fetchmany.assert_not_called()

if __name__ == '__main__':
    # Add some helpful output
    print("Running PostgreSQL connection tests...")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2)