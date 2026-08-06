from asset import Asset
from market_data import MarketData
from views import (
    show_portfolio,
    show_analysis,
    show_allocation,
    loading,
    show_historical_performance
)
from report import Report


class Portfolio:

    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def view_portfolio(self):

        if not self.assets:

            print("\nPortfolio is empty.")

            return

        show_portfolio(self.assets)

    def portfolio_allocation(self):

        if not self.assets:
            print("\nPortfolio is empty.")
            return

        total_current_value = 0

        # First pass - calculate total portfolio value
        for asset in self.assets:

            current_price = MarketData.get_asset_info(asset.ticker)["price"]

            analysis = asset.analyze(current_price)

            total_current_value += analysis["current_value"]

        rows = []

        # Second pass - calculate allocations
        for asset in self.assets:

            current_price = MarketData.get_asset_info(asset.ticker)["price"]

            analysis = asset.analyze(current_price)

            allocation = (
                analysis["current_value"] / total_current_value
            ) * 100

            rows.append(
                {
                    "ticker": analysis["ticker"],
                    "company": analysis["company"],
                    "value": analysis["current_value"],
                    "allocation": allocation
                }
            )

        show_allocation(rows) 

    def analyze_portfolio(self):

        if not self.assets:
            print("\nPortfolio is empty.")
            return

        rows = []

        total_investment = 0
        total_current_value = 0

        best_asset = None
        worst_asset = None
        largest_asset = None
        with loading("Fetching live market data..."):
            for asset in self.assets:

                current_price = MarketData.get_asset_info(asset.ticker)["price"]

                analysis = asset.analyze(current_price)
                if best_asset is None or analysis["return_percent"] > best_asset["return_percent"]:
                    best_asset = analysis

                if worst_asset is None or analysis["return_percent"] < worst_asset["return_percent"]:
                    worst_asset = analysis

                if largest_asset is None or analysis["current_value"] > largest_asset["current_value"]:
                    largest_asset = analysis

                rows.append(analysis)

                total_investment += analysis["investment"]
                total_current_value += analysis["current_value"]

        total_profit = total_current_value - total_investment

        overall_return = (
            total_profit / total_investment * 100
            if total_investment > 0
            else 0
        )

        summary = {
            "assets": len(self.assets),
            "investment": total_investment,
            "current_value": total_current_value,
            "profit": total_profit,
            "return": overall_return,
            

            "best": best_asset,
            "worst": worst_asset,
            "largest": largest_asset
        }

        show_analysis(rows, summary)

        return rows, summary

    def remove_asset(self, ticker):

        ticker = ticker.upper()

        for asset in self.assets:

            if asset.ticker == ticker:

                self.assets.remove(asset)

                print(f"\n{ticker} removed successfully!")

                return

        print(f"\n{ticker} not found in portfolio.")  


    def add_asset_interactive(self):

        ticker = input("\nTicker: ").upper()

        print("\nFetching market data...")

        try:

            data = MarketData.get_asset_info(ticker)

            print("-" * 45)
            print(f"Company       : {data['company']}")
            print(f"Current Price : ${data['price']:.2f}")
            print("-" * 45)

            buy_price = input(
                "\nPurchase Price (Press ENTER for current market price): "
            )

            if buy_price == "":
                buy_price = data["price"]
            else:
                buy_price = float(buy_price)

            # quantity = int(input("Quantity: "))
            while True:
                try:
                    quantity = float(input("Quantity: "))

                    if quantity <= 0:
                        print("❌ Quantity must be greater than 0.")
                        continue

                    break

                except ValueError:
                    print("❌ Please enter a valid number.")

            asset = Asset(
                data["ticker"],
                data["company"],
                quantity,
                buy_price
            )

            self.add_asset(asset)

            print(f"\n {data['company']} added successfully!")

        except Exception:

            print("\n Invalid ticker or network error.")      

    def search_asset(self):

        if not self.assets:
            print("\nPortfolio is empty.")
            return

        ticker = input("\nEnter ticker: ").upper()

        for asset in self.assets:

            if asset.ticker == ticker:

                show_portfolio([asset])

                return

        print(f"\n{ticker} not found in portfolio.")        

    def sort_portfolio(self):

        if not self.assets:
            print("\nPortfolio is empty.")
            return

        print("\nSort By")
        print("1. Ticker")
        print("2. Company")
        print("3. Quantity")
        print("4. Buy Price")

        choice = input("\nChoose option: ")

        if choice == "1":
            sorted_assets = sorted(self.assets, key=lambda asset: asset.ticker)

        elif choice == "2":
            sorted_assets = sorted(self.assets, key=lambda asset: asset.company)

        elif choice == "3":
            sorted_assets = sorted(
                self.assets,
                key=lambda asset: asset.quantity,
                reverse=True
            )

        elif choice == "4":
            sorted_assets = sorted(
                self.assets,
                key=lambda asset: asset.buy_price,
                reverse=True
            )

        else:
            print("\nInvalid option.")
            return

        show_portfolio(sorted_assets)    

    def edit_asset(self):

        if not self.assets:
            print("\nPortfolio is empty.")
            return

        ticker = input("\nEnter ticker to edit: ").upper()

        for asset in self.assets:

            if asset.ticker == ticker:

                print(f"\nEditing {asset.ticker}")
                print(f"Current Quantity : {asset.quantity}")
                print(f"Current Buy Price: ${asset.buy_price:.2f}")

                quantity = input("\nNew Quantity (Press ENTER to keep current): ")

                if quantity != "":
                    asset.quantity = float(quantity)

                buy_price = input("New Buy Price (Press ENTER to keep current): ")

                if buy_price != "":
                    asset.buy_price = float(buy_price)

                print(f"\n{ticker} updated successfully!")

                return

        print(f"\n{ticker} not found in portfolio.")    

    def historical_performance(self):

        ticker = input("\nEnter ticker: ").upper()

        print("\nChoose Period")
        print("1. 1 Month")
        print("2. 3 Months")
        print("3. 6 Months")
        print("4. 1 Year")

        choice = input("\nChoice: ")

        periods = {
            "1": "1mo",
            "2": "3mo",
            "3": "6mo",
            "4": "1y"
        }

        if choice not in periods:
            print("\nInvalid option.")
            return

        try:

            data = MarketData.get_historical_data(
                ticker,
                periods[choice]
            )

            show_historical_performance(
                ticker,
                periods[choice],
                data
            )

        except Exception:

            print("\nUnable to fetch historical data.")   

    def export_report(self):

        rows, summary = self.analyze_portfolio()

        Report.export_pdf(rows, summary)         