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
    'enableRateLimit': True,
})

# fetch_balance [x], fetch_positions [x], fetch_orders [x] (fees not implemented, but fetch_trades has fees), fetch_my_trades [x] ('side' doesnt show for funding trades)
bitmexExchange = ccxt.bitmex({
    'apiKey': os.environ.get('bitmex_key'),
    'secret': os.environ.get('bitmex_secret'),
    'enableRateLimit': True,
})
# for bitmex testnet https://github.com/ccxt/ccxt/issues/5717
bitmexExchange.urls['api'] = bitmexExchange.urls['test']

# fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
bybitExchange = ccxt.bybit({
    'apiKey': os.environ.get('bybit_key'),
    'secret': os.environ.get('bybit_secret'),
    'enableRateLimit': True,
    'options': {
         'defaultType': 'linear'
    }
})
bybitExchange.urls['api'] = bybitExchange.urls['test']

# fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
binanceExchange = ccxt.binanceusdm({
    'apiKey': os.environ.get('binance_key'),
    'secret': os.environ.get('binance_secret'),
    'enableRateLimit': True,
    # 'options': {
    #      'defaultType': 'future', # USD-M
    #     #'defaultType': 'delivery', # COIN-M
    #     #'defaultType': 'spot', # COIN-M
    #     'leverageBrackets': None,
    # },
})

# fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
phemexExchange = ccxt.phemex({
    'apiKey': os.environ.get('phemex_key'),
    'secret': os.environ.get('phemex_secret'),
    'enableRateLimit': True,
})
phemexExchange.urls['api'] = phemexExchange.urls['test']

okexExchange = ccxt.okex5({
    'apiKey': os.environ.get('okex_key'),
    'secret': os.environ.get('okex_secret'),
    'password': os.environ.get('okex_password'),
    'enableRateLimit': True,
    'headers': {
        'x-simulated-trading': '1',
    },
})
okexExchange.set_sandbox_mode(True)

def test_exchange_methods(exchange):
    print(exchange.name)
    #print('##########\nfetch_balance\n##########')
    # pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_open_orders())
    #print('##########\nfetch_positions\n##########')
    pprint(exchange.fetch_positions())
    #print(exchange.fetch_positions(None, {'currency': 'BTC'})) # ph emex - make ts call that calls all
    #pprint(exchange.fetch_positions(None, {'type': 'all'})) # bybit
    #print('##########\nfetch_orders\n##########')
    #pprint(exchange.fetch_orders())
    # pprint(exchange.fetch_open_orders('LINK/USDT', None, None)) # phemex /  bybit
    # pprint(exchange.fetch_orders()) # phemex /  bybit
    # pprint(exchange.fetch_open_orders())
    # print('##########\nfetch_my_trades\n##########')
    #pprint(exchange.fetch_my_trades())
    # print(exchange.fetch_my_trades('BTC/USD', None, None))


def main():
    #test_exchange_methods(ftxExchange)
    #test_exchange_methods(bitmexExchange)
    #test_exchange_methods(bybitExchange)
    # test_exchange_methods(binanceExchange)
    # test_exchange_methods(binanceExchange)
    test_exchange_methods(okexExchange)

if __name__ == "__main__":
    main()