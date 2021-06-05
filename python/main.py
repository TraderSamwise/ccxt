import os
from pprint import pprint

import ccxt

# exchanges
ftxExchange = ccxt.ftx({
    'apiKey': os.environ.get('ftx_key'),
    'secret': os.environ.get('ftx_secret'),
    'enableRateLimit': True
})
bitmexExchange = ccxt.bitmex({
    'apiKey': os.environ.get('bitmex_key'),
    'secret': os.environ.get('bitmex_secret'),
    'enableRateLimit': True
})
bybitExchange = ccxt.bybit({
    'apiKey': os.environ.get('bybit_key'),
    'secret': os.environ.get('bybit_secret'),
    'enableRateLimit': True
})
binanceExchange = ccxt.binance({
    'apiKey': os.environ.get('binance_key'),
    'secret': os.environ.get('binance_secret'),
    'enableRateLimit': True
})
phemexExchange = ccxt.phemex({
    'apiKey': os.environ.get('phemex_key'),
    'secret': os.environ.get('phemex_secret'),
    'enableRateLimit': True
})



def test_exchange_methods(exchange):
    print(exchange.name)
    pprint(exchange.fetch_positions())
    pprint(exchange.fetch_orders())


def main():
    test_exchange_methods(ftxExchange)
    test_exchange_methods(bitmexExchange)
    test_exchange_methods(bybitExchange)
    test_exchange_methods(binanceExchange)
    test_exchange_methods(phemexExchange)


if __name__ == "__main__":
    main()