CREATE MATERIALIZED VIEW daily_portfolio_history AS
WITH daily_prices AS (
    SELECT 
        date,
        ticker,
        close_price
    FROM ticker_daily
),
holdings_by_date AS (
    SELECT 
        t.portfolio_id,
        t.ticker,
        dp.date,
        SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.quantity ELSE -t.quantity END) 
        OVER (PARTITION BY t.portfolio_id, t.ticker ORDER BY t.transaction_date) as running_quantity,
        SUM(CASE WHEN t.transaction_type = 'BUY' THEN t.total_amount ELSE -t.total_amount END) 
        OVER (PARTITION BY t.portfolio_id, t.ticker ORDER BY t.transaction_date) as running_cost
    FROM transaction t
    CROSS JOIN daily_prices dp
    WHERE t.transaction_date::date <= dp.date
      AND t.transaction_type IN ('BUY', 'SELL')
),
daily_valuations AS (
    SELECT 
        hbd.portfolio_id,
        hbd.date,
        hbd.ticker,
        hbd.running_quantity as quantity,
        hbd.running_cost as cost_basis,
        dp.close_price,
        hbd.running_quantity * dp.close_price as market_value
    FROM holdings_by_date hbd
    JOIN daily_prices dp ON hbd.ticker = dp.ticker AND hbd.date = dp.date
    WHERE hbd.running_quantity > 0
)
SELECT 
    portfolio_id,
    date,
    SUM(market_value) as total_market_value,
    SUM(cost_basis) as total_cost_basis,
    SUM(market_value - cost_basis) as total_unrealized_gain_loss,
    (SUM(market_value - cost_basis) / SUM(cost_basis)) * 100 as total_return_percent,
    COUNT(*) as total_positions
FROM daily_valuations
GROUP BY portfolio_id, date;