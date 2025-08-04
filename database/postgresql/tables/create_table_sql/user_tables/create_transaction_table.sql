CREATE TABLE IF NOT EXISTS transaction (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolio(portfolio_id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    quantity DECIMAL(15,6) NOT NULL,
    transaction_type VARCHAR(4) NOT NULL, -- BUY, SELL
    price DECIMAL(15,6) NOT NULL,
    total_amount DECIMAL(15,6) NOT NULL,
    transaction_date TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);



-- Transaction indexes
CREATE INDEX IF NOT EXISTS idx_transaction_portfolio_id ON transaction(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_transaction_ticker ON transaction(ticker);
CREATE INDEX IF NOT EXISTS idx_transaction_date ON transaction(transaction_date);