# portfolio-tracker

INSERT INTO accounts (username, email, password_hash)
    VALUES ('test_username', 'test_email@gmail.com', 'test_password_hash')
    
INSERT INTO portfolios (portfolio_name, account_id)
VALUES ('test_portfolio', 'fd6c3bbf-434e-4848-916a-29b974c47ad2')
ON CONFLICT (account_id, portfolio_name) DO NOTHING
RETURNING portfolio_name

INSERT INTO portfolio_holdings (portfolio_id, ticker, quantity)
VALUES ('bb2cf94c-1c62-4056-9f5a-290c8487dfe7', 'SOFI', '15')
ON CONFLICT (portfolio_id, ticker) DO UPDATE
SET
    quantity = EXCLUDED.quantity,
    updated_at = CURRENT_TIMESTAMP