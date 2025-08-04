CREATE MATERIALIZED VIEW portfolio_valuations AS
WITH latest_prices AS (
    SELECT DISTINCT ON (ticker) 
        ticker, 
        price as current_price,
        time as price_time
    FROM ticker_prices 
    ORDER BY ticker, time DESC
),
portfolio_totals AS (
    SELECT 
        ch.portfolio_id,
        SUM(ch.quantity * lp.current_price) as total_market_value,
        SUM(ch.total_cost) as total_cost_basis
    FROM current_holdings ch
    JOIN latest_prices lp ON ch.ticker = lp.ticker
    GROUP BY ch.portfolio_id
)
SELECT 
    ch.portfolio_id,
    ch.ticker,
    ch.quantity,
    ch.avg_cost_per_share,
    ch.total_cost as cost_basis,
    lp.current_price,
    lp.price_time,
    (ch.quantity * lp.current_price) as market_value,
    (ch.quantity * lp.current_price) - ch.total_cost as unrealized_gain_loss,
    ((ch.quantity * lp.current_price) - ch.total_cost) / ch.total_cost * 100 as gain_loss_percent,
    pt.total_market_value as portfolio_total_value,
    pt.total_cost_basis as portfolio_total_cost,
    ROUND(((ch.quantity * lp.current_price) / pt.total_market_value) * 100, 4) as weight_percent,
    now() as calculated_at
FROM current_holdings ch
JOIN latest_prices lp ON ch.ticker = lp.ticker
JOIN portfolio_totals pt ON ch.portfolio_id = pt.portfolio_id;
