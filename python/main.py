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
okexExchange.set_sandbox_mode(True)

def test_exchange_get_methods(exchange):
    print(exchange.name)
    #print('##########\nfetch_balance\n##########')
    # pprint(exchange.fetch_markets())
    pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_open_orders())
    # pprint(exchange.fetch_open_orders(params={'type': 'oco'}))
    #print('##########\nfetch_positions\n##########')
    # pprint(exchange.fetch_positions())
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000, params={'stopPrice': None, 'timeInForce': 'PO', 'reduceOnly': True, 'trigger': None, 'closeOnTrigger': None})
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000)
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000, params={ 'timeInForce': 'PO', 'reduceOnly': True, 'trigger': None, 'closeOnTrigger': None})
    #print(exchange.fetch_positions(None, {'currency': 'BTC'})) # ph emex - make ts call that calls all
    #pprint(exchange.fetch_positions(None, {'type': 'all'})) # bybit
    #print('##########\nfetch_orders\n##########')
    # pprint(exchange.fetch_orders())
    # pprint(exchange.fetch_open_orders('BTC/USD', None, None)) # phemex /  bybit
    # pprint(exchange.fetch_orders()) # phemex /  bybit
    #pprint(exchange.fetch_open_orders())
    # print('##########\nfetch_my_trades\n##########')
    #pprint(exchange.fetch_my_trades())
    # print(exchange.fetch_my_trades('BTC/USD', None, None))

orders = []

def test_create_order(exchange, args):
    print('༼ つ ◕_◕ ༽つ =========================')
    print('create_order(', *args, ')')
    result = exchange.create_order(*args)
    return result

def test_exchange_post_methods(exchange):
    symbol = 'BTC/USD'
    size = 1
    ticker = exchange.fetch_ticker(symbol)
    last = ticker['last']

    print(exchange.name)

    print("Market buy, post only = true.")
    result = test_create_order(exchange, [
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
    # order = exchange.fetch_order(result['id'], symbol)
    assert result['postOnly'] == True

    print("Limit buy below last, reduce only = false and post only = false.")
    result = test_create_order(exchange, [
        symbol,
        'limit',
        'buy',
        size,
        last * 0.95,
        {
            'stopPrice': None,
            'timeInForce': 'GTC',  # GTC, PO
            'reduceOnly': False,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    order = exchange.fetch_order(result['id'], symbol)
    assert result['postOnly'] == True and result['reduceOnly']



def main():
    # test_exchange_get_methods(ftxExchange)
    # test_exchange_get_methods(bitmexExchange)
    # test_exchange_get_methods(bybitExchange)
    # test_exchange_get_methods(binanceExchange)
    # test_exchange_get_methods(phemexExchange)
    # test_exchange_get_methods(okexExchange)
    # test_exchange_post_methods(ftxExchange)
    # test_exchange_post_methods(bitmexExchange)
    test_exchange_post_methods(bybitExchange)
    # test_exchange_post_methods(binanceExchange)
    # test_exchange_post_methods(phemexExchange)
    # test_exchange_post_methods(okexExchange)

if __name__ == "__main__":
    main()