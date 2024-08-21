import MetaTrader5 as Mt5


class Trader:
    def __init__(self, symbol, account, password, server):
        self.symbol = symbol
        self.account = account
        self.password = password
        self.server = server

    def connect(self):
        if not Mt5.initialize():
            print("Falha ao inicializar o MT5")
            return False

        authorized = Mt5.login(self.account, password=self.password, server=self.server)
        if not authorized:
            print(f"Falha ao fazer login na conta {self.account}")
            print(f"Erro: {Mt5.last_error()}")
            Mt5.shutdown()
            return False

        print()
        print(f"Login bem-sucedido na conta {self.account}")
        return True

    @staticmethod
    def disconnect():
        Mt5.shutdown()

    def has_open_positions(self):
        positions = Mt5.positions_get(symbol=self.symbol)
        return len(positions) > 0

    def trade(self, action):
        if self.has_open_positions():
            print(f"Há uma ordem em aberto para o símbolo {self.symbol}.")
            print()
            return

        if action == 1:
            order_type = Mt5.ORDER_TYPE_BUY
            price = Mt5.symbol_info_tick(self.symbol).ask
            stop_loss = price - 100 * Mt5.symbol_info(self.symbol).point  # SL de 100 pontos
            take_profit = price + 5 * Mt5.symbol_info(self.symbol).point  # TP de 15 pontos
        elif action == 0:
            order_type = Mt5.ORDER_TYPE_SELL
            price = Mt5.symbol_info_tick(self.symbol).bid
            stop_loss = price + 100 * Mt5.symbol_info(self.symbol).point  # SL de 100 pontos
            take_profit = price - 5 * Mt5.symbol_info(self.symbol).point  # TP de 15 pontos
        else:
            print("Ação desconhecida:", action)
            return

        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": 60.0,  # ajuste o volume conforme necessário
            "type": order_type,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit,
            "deviation": 20,
            "magic": 234000,
            "comment": "comentário",
            "type_time": Mt5.ORDER_TIME_GTC,
            "type_filling": Mt5.ORDER_FILLING_RETURN,
        }

        result = Mt5.order_send(request)

        if result.retcode != Mt5.TRADE_RETCODE_DONE:
            print("Erro ao enviar a ordem:", result.comment)
            return

        print("Ordem enviada com sucesso, ticket:", result.order)
        print()
