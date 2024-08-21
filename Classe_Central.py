import MetaTrader5 as Mt5
import time
from datetime import datetime

from Classe_BarClassifier import BarClassifier
from Classe_Modelo import Modelo
from Classe_Trader15 import Trader
# from Class_Medium import MT5Trader
from Class_Profit_or_Loss import MT5Handler


def get_daily_profit(account, password, server):
    """
    Function to get the daily profit from MetaTrader5.
    """
    # Initialize MT5
    if not Mt5.initialize():
        print("Failed to initialize MT5")
        return 0

    # Login to the account
    authorized = Mt5.login(account, password, server=server)
    if not authorized:
        print(f"Failed to login to account {account}")
        Mt5.shutdown()
        return 0

    # Get the history of deals for the current day
    today = datetime.today()
    midnight = datetime(today.year, today.month, today.day)

    # Request history deals from midnight to now
    deals = Mt5.history_deals_get(midnight, datetime.now())

    if deals is None:
        print("No deals found.")
        Mt5.shutdown()
        return 0

    # Calculate profit from deals
    profit = 0
    for deal in deals:
        profit += deal.profit

    # Disconnect from MT5
    Mt5.shutdown()
    return profit


def main():

    """
    Main function that connects to MetaTrader5, gets bar data,
    classifies bars, loads the machine learning model,
    makes predictions and executes trades based on predictions.
    """
    # MT5 account settings
    account = 52014956  # Replace with your account number
    password = "16a91Gj#"  # Replace with your account password
    server = "XPMT5-DEMO"  # Replace with your server name

    # Asset and timeframe settings
    symbol = "WINV24"
    timeframe = Mt5.TIMEFRAME_M1

    # num_bars = 8  # Number of bars to consider
    #
    # trader = MT5Trader(account, password, server, symbol, timeframe, num_bars)
    # difference = trader.print_min_max_difference()
    # print()
    #
    # # Check if the difference is within the allowed range
    # if difference <= 200 or difference >= 700:
    #     while True:
    #         trader = MT5Trader(account, password, server, symbol, timeframe, num_bars)
    #         difference = trader.print_min_max_difference()
    #         if 200 < difference < 700:
    #             print("Resuming execution.")
    #             print()
    #             break
    #         # time.sleep(60)

    mt5_handler = MT5Handler(account, password, server)

    if not mt5_handler.connect():
        return

    last_order_profit = MT5Handler.get_last_closed_order_profit()

    if last_order_profit is None:
        print("Could not determine the profit of the last closed order.")
    else:
        if last_order_profit > 0:
            print(f"\033[32mThe last closed order's profit was: {last_order_profit:.2f}\033[m")
            print()
        else:
            print(f"\033[31mThe last closed order's profit was: {last_order_profit:.2f}\033[m")
            print()

    mt5_handler.disconnect()

    # Initialize the bar classifier
    bar_classifier = BarClassifier(symbol, timeframe)

    # Connect to MetaTrader5
    if not bar_classifier.connect(account, password, server):
        return

    # Get the last 9 bars
    rates = bar_classifier.get_last_bars()

    # Check if rates is None
    if rates is None:
        bar_classifier.disconnect()
        return

    # Classify the bars
    classifications = bar_classifier.classify_bars(rates)
    print("Bar classifications:", classifications)

    # Load the model and make the prediction
    modelo = Modelo('modelo_treinado.pkl', classifications)  # Replace with your model file name
    prediction = modelo.funcao_modelo()

    # Initialize the Trader
    trader = Trader(symbol, account, password, server)
    if not trader.connect():
        bar_classifier.disconnect()
        return

    # Execute the trade based on the prediction4
    trader.trade(prediction[0])

    # Disconnect from MetaTrader5
    bar_classifier.disconnect()
    trader.disconnect()


if __name__ == "__main__":
    target_profit = int(input("Enter the target daily profit: "))  # User-defined target profit
    stop_loss = int(input("Enter the daily stop loss: "))  # User-defined daily stop loss
    print()
    last_minute = -1

    while True:

        # Get the current hour and minute
        current_hour = int(time.strftime('%H'))
        current_minute = int(time.strftime('%M'))

        # Check if the current hour is between 9:00 and 18:20
        if ((current_hour > 9 or (current_hour == 9 and current_minute >= 8)) and
                (current_hour < 19 or (current_hour == 19 and current_minute <= 20))):
            # Check if the minute is different from the last minute executed
            if current_minute != last_minute:
                daily_profit = get_daily_profit(52014956, "16a91Gj#", "XPMT5-DEMO")
                if daily_profit > 0:
                    print('Atualizando...')
                    print()
                    print(f"\033[32mCurrent daily profit: {daily_profit:.2f}\033[m")
                elif daily_profit < 0:
                    print('Atualizando...')
                    print()
                    print(f"\033[31mCurrent daily profit: {daily_profit:.2f}\033[m")
                else:
                    print('Atualizando...')
                    print()
                    print(f"\033[37mCurrent daily profit: {daily_profit:.2f}\033[m")

                # Check if the daily profit has reached or exceeded the target profit
                if daily_profit >= target_profit:
                    print(f"Target daily profit of {target_profit:.2f} reached. Stopping execution.")
                    break

                # Check if the daily profit has fallen below the stop loss
                if daily_profit <= stop_loss:
                    print(f"Daily stop loss of {stop_loss:.2f} reached. Stopping execution.")
                    break

                # time.sleep(1.5)

                main()
                last_minute = current_minute
