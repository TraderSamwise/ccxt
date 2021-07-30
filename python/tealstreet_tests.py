import os
from pprint import pprint

import ccxt

# exchanges

# fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
import pytest

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
    'enableRateLimit': True
})
bybitExchange.set_sandbox_mode(True)

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

okexExchange = ccxt.okex({
    'apiKey': os.environ.get('okex_key'),
    'secret': os.environ.get('okex_secret'),
    'password': os.environ.get('okex_password'),
    'enableRateLimit': True,
    'headers': {
        'x-simulated-trading': '1',
    },
})
__test__ = True
okexExchange.set_sandbox_mode(True)

orders = []
exchange = bybitExchange

def do_create_order(args):
    print('༼ つ ◕_◕ ༽つ =========================')
    print('create_order(', *args, ')')
    result = exchange.create_order(*args)
    return result


symbol = 'BTC/USD'
size = 1
ticker = exchange.fetch_ticker(symbol)
last = ticker['last']

print(exchange.name)

print("Market buy, post only = true.")
result = do_create_order([
    symbol,
    'market',
    'buy',
    size,
    None,
    {
        'stopPrice': None,
        'timeInForce': 'PO', # GTC, PO
        'reduceOnly': False,
        'trigger': None,
        'closeOnTrigger': None,
        'basePrice': None
    }
])
order = exchange.fetch_order(result['id'], symbol)
assert result['postOnly'] == True
#
# print("Limit buy below last, reduce only = false and post only = false.")
# result = test_create_order(exchange, [
#     symbol,
#     'limit',
#     'buy',
#     size,
#     last * 0.95,
#     {
#         'stopPrice': None,
#         'timeInForce': 'GTC',  # GTC, PO
#         'reduceOnly': False,
#         'trigger': None,
#         'closeOnTrigger': None,
#         'basePrice': None
#     }
# ])
# order = exchange.fetch_order(result['id'], symbol)
# assert result['postOnly'] == True and result['reduceOnly']