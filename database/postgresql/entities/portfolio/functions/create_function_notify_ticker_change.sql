-- Create function to notify update
-- This is so that we can add the new tickers to our active:tickers key stored in Redis
CREATE OR REPLACE FUNCTION notify_ticker_change() RETURNS trigger AS $$
DECLARE
    payload TEXT;
BEGIN
    IF TG_OP = 'DELETE' THEN
        payload := json_build_object('operation', TG_OP, 'ticker', OLD.ticker)::TEXT;
    ELSE
        payload := json_build_object('operation', TG_OP, 'ticker', NEW.ticker)::TEXT;
    END IF;

    PERFORM pg_notify('portfolio_ticker_change', payload);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql
