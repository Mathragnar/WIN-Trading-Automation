import MetaTrader5 as Mt5
from datetime import datetime, timedelta


class MT5Handler:
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        self.server = server

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

    @staticmethod
    def get_last_closed_order_profit():
        now = datetime.now()
        from_date = now - timedelta(days=30)  # Buscar negociações dos últimos 30 dias
        deals = Mt5.history_deals_get(from_date, now)

        if deals is None or len(deals) == 0:
            print("No deals found.")
            return None

        # Filtrar apenas as negociações fechadas que têm lucro/prejuízo definido
        closed_deals = [deal for deal in deals if
                        deal.type in (Mt5.DEAL_TYPE_BUY, Mt5.DEAL_TYPE_SELL) and deal.profit != 0]

        if not closed_deals:
            print("No closed deals found.")
            return None

        # Ordenar as negociações pelo tempo de execução e pegar a última
        last_deal = sorted(closed_deals, key=lambda d: d.time, reverse=True)[0]

        return last_deal.profit
