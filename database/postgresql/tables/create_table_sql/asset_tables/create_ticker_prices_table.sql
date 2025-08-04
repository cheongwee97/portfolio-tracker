CREATE TABLE IF NOT EXISTS ticker_prices (
    time TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    price DECIMAL(15,6) NOT NULL,
    volume BIGINT,
    bid DECIMAL(15,6),
    ask DECIMAL(15,6),
    change_percent DECIMAL(8,4),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ticker_prices_time_ticker ON ticker_prices(time, ticker);
CREATE INDEX IF NOT EXISTS idx_ticker_prices_ticker_time ON ticker_prices(ticker, time DESC);

