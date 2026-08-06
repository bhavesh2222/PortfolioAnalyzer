class Asset:
    """
    Represents a single stock/crypto in the portfolio.
    """

    def __init__(self, ticker, company, quantity, buy_price):

        self.ticker = ticker.upper()
        self.company = company
        self.quantity = quantity
        self.buy_price = buy_price

    def __str__(self):
        return (
            f"{self.ticker:<10}"
            f"{self.company:<25}"
            f"{self.quantity:<8}"
            f"${self.buy_price:<10.2f}"
        )
    def investment_value(self):
        return self.quantity * self.buy_price
    
    def current_value(self, current_price):
        return self.quantity * current_price

    def profit(self, current_price):
        return self.current_value(current_price) - self.investment_value()

    def return_percentage(self, current_price):

        return (
            self.profit(current_price)
            /
            self.investment_value()
        ) * 100

    def analyze(self, current_price):

        investment = self.investment_value()

        current_value = self.current_value(current_price)

        profit = self.profit(current_price)

        returns = self.return_percentage(current_price)

        return {
            "ticker": self.ticker,
            "company": self.company,
            "quantity": self.quantity,
            "buy_price": self.buy_price,
            "current_price": current_price,
            "investment": investment,
            "current_value": current_value,
            "profit": profit,
            "return_percent": returns
        }