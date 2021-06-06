import os
from pprint import pprint

import ccxt

# exchanges

# fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
ftxExchange = ccxt.ftx({
    'apiKey': os.environ.get('ftx_key'),
    'secret': os.environ.get('ftx_secret'),
    'headers': {
        'FTX-SUBACCOUNT': 'APITEST',
    },
    'enableRateLimit': True
})
# fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
bitmexExchange = ccxt.bitmex({
    'apiKey': os.environ.get('bitmex_key'),
    'secret': os.environ.get('bitmex_secret'),
    'enableRateLimit': True
})
# fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
bybitExchange = ccxt.bybit({
    'apiKey': os.environ.get('bybit_key'),
    'secret': os.environ.get('bybit_secret'),
    'enableRateLimit': True
})
# fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
binanceExchange = ccxt.binance({
    'apiKey': os.environ.get('binance_key'),
    'secret': os.environ.get('binance_secret'),
    'enableRateLimit': True
})
# fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
phemexExchange = ccxt.phemex({
    'apiKey': os.environ.get('phemex_key'),
    'secret': os.environ.get('phemex_secret'),
    'enableRateLimit': True
})


def test_exchange_methods(exchange):
    print(exchange.name)
    print('##########\nfetch_balance\n##########')
    pprint(exchange.fetch_balance())
    print('##########\nfetch_positions\n##########')
    pprint(exchange.fetch_positions())
    print('##########\nfetch_orders\n##########')
    pprint(exchange.fetch_orders())
    print('##########\nfetch_my_trades\n##########')
    pprint(exchange.fetch_my_trades())


def main():
    test_exchange_methods(ftxExchange)
    #test_exchange_methods(bitmexExchange)
    #test_exchange_methods(bybitExchange)
    #test_exchange_methods(binanceExchange)
    #test_exchange_methods(phemexExchange)


if __name__ == "__main__":
    main()