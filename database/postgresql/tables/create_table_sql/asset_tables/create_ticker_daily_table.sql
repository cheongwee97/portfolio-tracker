CREATE TABLE IF NOT EXISTS ticker_daily (
    date DATE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    open_price DECIMAL(15,6) NOT NULL,
    high_price DECIMAL(15,6) NOT NULL,
    low_price DECIMAL(15,6) NOT NULL,
    close_price DECIMAL(15,6) NOT NULL,
    adjusted_close DECIMAL(15,6) NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (date, ticker)
);

CREATE INDEX IF NOT EXISTS idx_ticker_daily_ticker_date ON ticker_daily(ticker, date DESC);