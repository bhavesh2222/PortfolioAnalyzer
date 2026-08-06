from portfolio import Portfolio
from storage import Storage
from views import show_banner

portfolio = Portfolio()
portfolio.assets = Storage.load()

while True:

    show_banner()
    print("1. Add Asset")
    print("2. Remove Asset")
    print("3. View Portfolio")
    print("4. Analyze Portfolio")
    print("5. Portfolio Allocation")
    print("6. Search Asset")
    print("7. Sort Portfolio")
    print("8. Edit Asset")
    print("9. Exit")

    choice = input("\nChoose option: ")

    if choice == "1":
        portfolio.add_asset_interactive()

    elif choice == "2":

        ticker = input("Enter ticker to remove: ")

        portfolio.remove_asset(ticker)

    elif choice == "3":

        portfolio.view_portfolio()
    elif choice == "4":

        portfolio.analyze_portfolio() 

    elif choice == "5":

        portfolio.portfolio_allocation()  

    elif choice == "6":

        portfolio.search_asset()   

    elif choice == "7":

        portfolio.sort_portfolio()    

    elif choice == "8":

        portfolio.edit_asset()            

    elif choice == "9":

        Storage.save(portfolio)

        print("\nPortfolio saved successfully!")

        print("Goodbye!")

        break

    else:

        print("\nInvalid Option.")

