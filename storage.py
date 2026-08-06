import csv

from asset import Asset


class Storage:

    FILE_NAME = "portfolio.csv"

    @staticmethod
    def save(portfolio):

        with open(Storage.FILE_NAME, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Ticker",
                    "Company",
                    "Quantity",
                    "BuyPrice"
                ]
            )

            for asset in portfolio.assets:

                writer.writerow(
                    [
                        asset.ticker,
                        asset.company,
                        asset.quantity,
                        asset.buy_price
                    ]
                )

    @staticmethod
    def load():

        portfolio = []

        try:

            with open(Storage.FILE_NAME, "r") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    asset = Asset(

                        row["Ticker"],

                        row["Company"],

                        float(row["Quantity"]),

                        float(row["BuyPrice"])

                    )

                    portfolio.append(asset)

        except FileNotFoundError:

            pass

        return portfolio

