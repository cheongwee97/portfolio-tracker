CREATE MATERIALIZED VIEW current_holdings AS
SELECT 
    portfolio_id,
    ticker,
    SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE -quantity END) as quantity,
    SUM(CASE WHEN transaction_type = 'BUY' THEN total_amount ELSE -total_amount END) as total_cost,
    SUM(CASE WHEN transaction_type = 'BUY' THEN total_amount ELSE -total_amount END) / 
    NULLIF(SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE -quantity END), 0) as avg_cost_per_share,
    MAX(transaction_date) as last_transaction_date
FROM transaction 
WHERE transaction_type IN ('BUY', 'SELL')
GROUP BY portfolio_id, ticker
HAVING SUM(CASE WHEN transaction_type = 'BUY' THEN quantity ELSE -quantity END) > 0;
