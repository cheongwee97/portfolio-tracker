import json
import select
from database.postgresql.utils.psql_conn import conn, query_table
from database.redis.utils.redis_conn import redis_client

conn.set_isolation_level(0)  # Autocommit required for LISTEN
cur = conn.cursor()
cur.execute("LISTEN portfolio_ticker_change;")
print("Listening for portfolio_ticker_change notifications...")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue  # timeout every 5s
    conn.poll()
    while conn.notifies:
        notify = conn.notifies.pop(0)

        try:
            data = json.loads(notify.payload)
            op = data.get("operation")
            ticker = data.get("ticker", "").upper()

            if not ticker:
                print("Missing ticker, skipping notification")
                continue

            if op == 'INSERT':
                redis_client.sadd("active:tickers", ticker)
                print(f"Added {ticker} to active:tickers")

            elif op == 'DELETE':
                query = """
                    SELECT 1 FROM portfolio_holdings WHERE ticker = %s LIMIT 1
                """
                exists = query_table(query, (ticker,))
                if not exists:
                    redis_client.srem("active:tickers", ticker)
                    print(f"Removed {ticker} from active:tickers")

        except Exception as e:
            print(f"Error processing notification: {e}")