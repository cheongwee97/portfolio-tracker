CREATE MATERIALIZED VIEW portfolio_summary AS
SELECT 
    portfolio_id,
    COUNT(*) as total_positions,
    SUM(market_value) as total_market_value,
    SUM(cost_basis) as total_cost_basis,
    SUM(unrealized_gain_loss) as total_unrealized_gain_loss,
    (SUM(unrealized_gain_loss) / SUM(cost_basis)) * 100 as total_gain_loss_percent,
    MAX(weight_percent) as largest_position_weight,
    COUNT(CASE WHEN weight_percent > 10 THEN 1 END) as positions_over_10_percent,
    -- Diversification metrics
    SUM(POWER(weight_percent/100, 2)) as concentration_ratio,
    CASE 
        WHEN SUM(POWER(weight_percent/100, 2)) > 0.25 THEN 'Highly Concentrated'
        WHEN SUM(POWER(weight_percent/100, 2)) > 0.15 THEN 'Moderately Concentrated'
        ELSE 'Well Diversified'
    END as diversification_level,
    MAX(calculated_at) as calculated_at
FROM portfolio_valuations
GROUP BY portfolio_id;