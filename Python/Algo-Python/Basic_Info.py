
from yahoo_fin import options
from yahoo_fin import stock_info


def get_stock():
    ticker = input("Stock Ticker: ")
    try:
        quote_table = stock_info.get_quote_table(ticker)

        # Bid and Ask formatted <price> x <volume>
        ask = float(quote_table.get("Ask").split()[0])
        bid = float(quote_table.get("Bid").split()[0])
        price = format((bid+ask)/2, "5.2f")
        print("\n"+format("Current Price", "27s"), price)

        # Info I care about
        useful_info = ["52 Week Range", "Market Cap", "Earnings Date",
                       "Forward Dividend & Yield", "PE Ratio (TTM)"]
        for info in useful_info:
            print(format(info, "27s"), quote_table.get(info))

    except:
        print('Unable to collect data on ' + ticker.upper())
        return(0)

    return(ticker)


ticker = get_stock()
