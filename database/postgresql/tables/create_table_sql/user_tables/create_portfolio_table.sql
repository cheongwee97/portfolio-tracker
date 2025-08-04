CREATE TABLE IF NOT EXISTS portfolio (
    portfolio_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
    portfolio_name VARCHAR(25) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);



-- Portfolio indexes
CREATE INDEX IF NOT EXISTS idx_portfolio_account_id ON portfolio(account_id);