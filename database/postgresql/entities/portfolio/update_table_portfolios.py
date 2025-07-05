from database.postgresql.tables.portfolio.obj.portfolio import Portfolio
from database.postgresql.tables.portfolio.obj.portfolio_holding import PortfolioHolding
from database.postgresql.utils.psql_conn import execute


def create_portfolio(portfolio: Portfolio) -> None:
    insert_query = """
        INSERT INTO portfolios (portfolio_name, account_id)
        VALUES (%s, %s)
        ON CONFLICT (account_id, portfolio_name) DO NOTHING
        RETURNING portfolio_name
    """
    result = execute(insert_query, (portfolio.portfolio_name, portfolio.account_id))
    if result:
        print(f"Portfolio created: {result[0]['portfolio_name']}")
    else:
        # Conflict happened, portfolio name is taken
        print(f"portfolio_name: {portfolio.portfolio_name} is taken")


def update_portfolio(portfolio_holding: PortfolioHolding) -> None:
    query_template = """
        INSERT INTO portfolio_holdings (portfolio_id, ticker, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (portfolio_id, ticker) DO UPDATE
        SET
            quantity = EXCLUDED.quantity,
            updated_at = CURRENT_TIMESTAMP
    """
    execute(query_template, (
        portfolio_holding.portfolio_id,
        portfolio_holding.ticker,
        portfolio_holding.quantity
    ))


def delete_portfolio(portfolio_id: str) -> None:
    query_template = """
        DELETE FROM portfolios
        WHERE portfolio_id = %s
    """
    affected_rows = execute(query_template, (portfolio_id,))
    if affected_rows == 0:
        print(f"No portfolio found with id: {portfolio_id}")
