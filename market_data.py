import yfinance as yf


class MarketData:

    @staticmethod
    def get_asset_info(ticker):

        stock = yf.Ticker(ticker)

        info = stock.info

        history = stock.history(period="1d")

        return {
            "ticker": ticker.upper(),
            "company": info.get("longName", "Unknown"),
            "price": history["Close"].iloc[-1]
        }