import MetaTrader5 as Mt5
from datetime import datetime, timedelta


class BarClassifier:
    def __init__(self, symbol, timeframe, bars_count=9):  # Modificado para 9
        self.symbol = symbol
        self.timeframe = timeframe
        self.bars_count = bars_count

    @staticmethod
    def connect(account, password, server):
        if not Mt5.initialize():
            print("Falha ao inicializar o MT5")
            return False

        if not Mt5.login(account, password=password, server=server):
            print(f"Falha ao fazer login na conta {account}")
            print(f"Erro: {Mt5.last_error()}")
            Mt5.shutdown()
            return False

        print(f"Login bem-sucedido na conta {account}")
        return True

    def get_last_bars(self):
        utc_from = datetime.now() - timedelta(minutes=self.bars_count * 5)  # Assumindo timeframe M1 (1 minuto)
        rates = Mt5.copy_rates_from(self.symbol, self.timeframe, utc_from, self.bars_count)

        if rates is None:
            print(f"Falha ao obter as últimas {self.bars_count} barras")
            return None

        return rates

    @staticmethod
    def classify_bars(rates):
        classifications = []
        for rate in rates:
            if rate['close'] > rate['open']:
                classifications.append(1)  # Barra de alta
            elif rate['close'] < rate['open']:
                classifications.append(0)  # Barra de baixa
            else:
                classifications.append(2)  # Barra sem spread

        # Exclui a última classificação
        if classifications:
            classifications = classifications[:-1]

        return classifications

    @staticmethod
    def disconnect():
        Mt5.shutdown()
