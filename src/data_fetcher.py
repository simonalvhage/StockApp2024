import yfinance as yf


class DataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_data = None

    def fetch_historical_data(self, period='1y', interval='1d'):
        self.stock_data = yf.download(self.ticker, period=period, interval=interval)
        return self.stock_data

    def get_latest_price(self):
        ticker_data = yf.Ticker(self.ticker)
        todays_data = ticker_data.history(period='1d')
        return todays_data['Close'][0] if not todays_data.empty else None
