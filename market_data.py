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

    @staticmethod
    def get_historical_data(ticker, period):

        stock = yf.Ticker(ticker)

        history = stock.history(period=period)

        if history.empty:
            raise Exception("No historical data found.")

        return {
            "start_price": history["Close"].iloc[0],
            "current_price": history["Close"].iloc[-1],
            "highest_price": history["High"].max(),
            "lowest_price": history["Low"].min(),
        }