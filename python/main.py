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
binanceExchange = ccxt.binancecoinm({
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
    result = exchange.create_order(
             'BTC-USD-SWAP',
        'stoplimit',
        'buy',
        1,
        35000,
        {
            'stopPrice': 48000,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Index',
            'closeOnTrigger': True,
            'basePrice': 23890
        })

    # exchange.cancel_order('18748454326', 'BTC/USD', params={'type': 'limit'})
    exchange.fetch_order('342273454577688576', 'BTC-USD-SWAP', params={'type': 'stop'})

    orders = [{'id': '18747457675', 'type': 'stop'}, {'id': '18747460710', 'type': 'stop'}, {'id': '18747461436', 'type': 'stop'}, {'id': '18747462096', 'type': 'stop'}, {'id': '18747462701', 'type': 'stop'}, {'id': '18747463265', 'type': 'stop'}, {'id': '18747463947', 'type': 'stop'}, {'id': '18747468725', 'type': 'stop'}]

    for order in orders:

        order_before = exchange.fetch_order(order['id'], 'BTC/USD')
        print('ORDER BEFORE')
        pprint(order_before)
        print('ORDER BEFORE')

        # result = exchange.create_order(
        #     'BTC/USD',
        #     'limit',
        #     'buy',
        #     1,
        #     40000,
        #     {
        #         'stopPrice': None,
        #         'timeInForce': 'GTC',  # GTC, PO
        #         'reduceOnly': False,
        #         'trigger': None,
        #         'closeOnTrigger': None,
        #         'basePrice': None
        #     })

        cancel_result = exchange.cancel_order(order['id'], 'BTC/USD')
        print('CANCEL RESULT')
        pprint(cancel_result)
        print('CANCEL RESULT')

        order_after = exchange.fetch_order(order['id'], 'BTC/USD')
        print('ORDER AFTER')
        pprint(order_after)
        print('ORDER AFTER')

        hi = True


    #print('##########\nfetch_balance\n##########')
    # pprint(exchange.fetch_markets())
    # pprint(exchange.fetch_balance())
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


def main():
    # test_exchange_get_methods(ftxExchange)
    # test_exchange_get_methods(bitmexExchange)
    # test_exchange_get_methods(bybitExchange)
    # test_exchange_get_methods(binanceExchange)
    # test_exchange_get_methods(phemexExchange)
    test_exchange_get_methods(okexExchange)

if __name__ == "__main__":
    main()