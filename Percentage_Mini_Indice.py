import MetaTrader5 as Mt5
import datetime
import time

# Conecta ao MetaTrader5
if not Mt5.initialize():
    print("initialize() failed, error code =", Mt5.last_error())
    quit()

# Símbolo desejado
symbol = "WINQ24"

# Flag para controlar o primeiro print
primeiro_print = True

while True:
    # Data de hoje
    today = datetime.date.today()

    # Obter o último tick de ontem (segundo último candle diário)
    rates_yesterday = Mt5.copy_rates_from_pos(symbol, Mt5.TIMEFRAME_D1, 1, 1)

    if rates_yesterday is None:
        print(f"Erro ao obter dados de ontem: {Mt5.last_error()}")
    else:
        # Preço de fechamento de ontem
        close_yesterday = rates_yesterday[0][4]

        # Obter o preço atual
        tick = Mt5.symbol_info_tick(symbol)

        if tick is None:
            print(f"Erro ao obter dados atuais: {Mt5.last_error()}")
        else:
            # Calcular a variação percentual
            variacao_percentual = ((tick.last - close_yesterday) / close_yesterday) * 100

            # Imprime a primeira vez sem \r, depois com \r
            if primeiro_print:
                print(f"Variação percentual diária de {symbol}: {variacao_percentual:.2f}%", end="")
                primeiro_print = False
            else:
                print(f"\rVariação percentual diária de {symbol}: {variacao_percentual:.2f}%", end="")

    # Aguarda 1 segundo antes da próxima iteração
    time.sleep(1)
