# portfolio-tracker

INSERT INTO accounts (username, email, password_hash)
    VALUES ('test_username', 'test_email@gmail.com', 'test_password_hash')
    
INSERT INTO portfolios (portfolio_name, account_id)
VALUES ('test_portfolio', '816e86bc-4aba-492e-ab38-3a40f47f4901')
ON CONFLICT (account_id, portfolio_name) DO NOTHING
RETURNING portfolio_name

INSERT INTO portfolio_holdings (portfolio_id, ticker, quantity)
VALUES ('70d008f2-9302-44d1-9c4a-a7ad4e443bdc', 'SOFI', '15')
ON CONFLICT (portfolio_id, ticker) DO UPDATE
SET
    quantity = EXCLUDED.quantity,
    updated_at = CURRENT_TIMESTAMP