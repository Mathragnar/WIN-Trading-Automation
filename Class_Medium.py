import MetaTrader5 as Mt5
from datetime import datetime, timedelta


class MT5Trader:
    def __init__(self, account, password, server, symbol, timeframe, num_bars):
        self.account = account
        self.password = password
        self.server = server
        self.symbol = symbol
        self.timeframe = timeframe
        self.num_bars = num_bars

    def connect(self):
        if not Mt5.initialize():
            print("Failed to initialize MT5")
            return False

        authorized = Mt5.login(self.account, password=self.password, server=self.server)
        if not authorized:
            print(f"Failed to login to account {self.account}")
            print(f"Error: {Mt5.last_error()}")
            Mt5.shutdown()
            return False

        print(f"Login successful on account {self.account}")
        return True

    @staticmethod
    def disconnect():
        Mt5.shutdown()

    def get_min_max_sum(self):
        utc_from = datetime.now() - timedelta(minutes=self.timeframe * self.num_bars)
        rates = Mt5.copy_rates_from(self.symbol, self.timeframe, utc_from, self.num_bars)

        if rates is None:
            print("No rates found.")
            return None, None

        min_sum = sum(rate['low'] for rate in rates)
        max_sum = sum(rate['high'] for rate in rates)

        return min_sum, max_sum

    def print_min_max_difference(self):
        if not self.connect():
            return

        min_sum, max_sum = self.get_min_max_sum()

        if min_sum is not None and max_sum is not None:
            # print(f"Sum of highs for the last {self.num_bars} bars: {max_sum:.2f}")
            # print(f"Sum of lows for the last {self.num_bars} bars: {min_sum:.2f}")
            # print(f"Difference (max_sum - min_sum): {max_sum - min_sum:.2f}")

            difference = max_sum - min_sum
            return difference

        self.disconnect()
