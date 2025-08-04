CREATE TABLE IF NOT EXISTS ticker_metadata (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    currency VARCHAR(3) DEFAULT 'USD',
    is_active BOOLEAN DEFAULT true,
    last_updated TIMESTAMPTZ DEFAULT now() NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ticker_metadata_active ON ticker_metadata(is_active);
CREATE INDEX IF NOT EXISTS idx_ticker_metadata_updated ON ticker_metadata(last_updated);