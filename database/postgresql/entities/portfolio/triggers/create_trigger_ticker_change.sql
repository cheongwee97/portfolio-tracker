-- Create trigger to notify portfolio insert or delete
DROP TRIGGER IF EXISTS trigger_ticker_change ON portfolio_holdings;
CREATE TRIGGER trigger_ticker_change
AFTER INSERT OR DELETE ON portfolio_holdings
FOR EACH ROW
EXECUTE FUNCTION notify_ticker_change();