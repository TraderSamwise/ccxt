import os
cwd = os.getcwd()
from pprint import pprint
import test_exchanges as test
import ccxt
from ccxt import errors
import time

def buy_stuff():
    exchange = test.mngz_ftx_exchange
    symbol = 'BTC-PERP'
    count = 0
    sleep_time = 5
    clear_buys = True

    response = exchange.api_referral_success()

    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            last = ticker['last']
            if last > 49700:
                buyprice = last * 0.995
                clear_buys = False
            else:
                buyprice = (last - 5)
                clear_buys = True
            print(buyprice)
            count += 1
            if count % 12 == 0 and clear_buys:
                orders = exchange.fetch_open_orders(symbol)
                for order in orders:
                    if order['side'] == 'buy':
                        try:
                            cancel_result = exchange.cancel_order(order['id'], symbol, { 'type': 'limit'})
                        except BaseException as err:
                            cancel_result = err
                        print(cancel_result)

            result = ''
            try:
                result = exchange.create_order(
                    symbol,
                    'limit',
                    'buy',
                    0.01,
                    buyprice,
                    {
                        'stopPrice': None,
                        'timeInForce': 'GTC',
                        'reduceOnly': None,
                        'closeOnTrigger': None,
                        'basePrice': None,
                        'trigger': None,
                    })
            except BaseException as err:
                result = err
            print(result)

            if last > 49700:
                try:
                    positions = exchange.fetch_positions(symbol)
                    position = [x for x in positions if x['symbol'] == symbol][0]

                    orders = exchange.fetch_open_orders(symbol)
                    total_sell = sum([x['amount'] for x in orders if x['symbol'] == symbol and x['side'] == 'sell'])
                    order_sell = position['contracts']-total_sell
                    if order_sell >= 0.01:
                        result = exchange.create_order(
                            symbol,
                            'limit',
                            'sell',
                            position['contracts']-total_sell,
                            last * 1.005,
                            {
                                'stopPrice': None,
                                'timeInForce': 'GTC',
                                'reduceOnly': True,
                                'closeOnTrigger': None,
                                'basePrice': None,
                                'trigger': None,
                            })
                        print(result)
                        time.sleep(1)
                except BaseException as err:
                    result = err
                    print(result)

            try:
                if '"success":false' not in str(result):
                    sleep_time = 1
                else:
                    sleep_time = 5
            except:
                sleep_time = 1

        except:
            print('error')

        time.sleep(sleep_time)
        
# BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE #
def test_binance():
    # exchange = test.mn_binance_usdm_exchange
    exchange = test.mn_binance_coinm_exchange

    symbol = 'BTC/USD'
    ticker = exchange.fetch_ticker(symbol)
    last = ticker['last']

    # exchange.edit_order('37677901237',
    #      'BTC/USD',
    #      'limit',
    #      'buy',
    #      1.0,
    #      40000.0,
    #      {
    #         'closeOnTrigger': None,
    #           'reduceOnly': None,
    #           'stopPrice': 0.0,
    #           'timeInForce': 'GTC',
    #           'trigger': 'Last'
    #     }
    # )

    # exchange.create_order(symbol,
    #                       'stop',
    #                       'sell',
    #                       0.001,
    #                       51001,
    #                       {
    #                           'stopPrice': 51000,
    #                           'timeInForce': 'PO',
    #                           'reduceOnly': None,
    #                           'trigger': 'Last',
    #                           'closeOnTrigger': False,
    #                           'basePrice': last
    #                       })
    # exchange.create_order(symbol,
    # 'stoplimit',
    # 'buy',
    # 1,
    # last * 0.94,
    # {
    #     'stopPrice': last * 1.06,
    #     'timeInForce': 'PO',
    #     'reduceOnly': None,
    #     'trigger': 'Last',
    #     'closeOnTrigger': False,
    #     'basePrice': last
    # })
    # pprint(exchange.fetch_open_orders('BTC/USD'))
    pprint(exchange.fetch_orders('BTC/USD'))
    # pprint(exchange.fetch_positions())
    # pprint(exchange.cancel_all_orders('BTC/USD'))
# BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE BINANCE #

# BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX #
def test_bitmex():
    exchange = test.tn_bitmex_exchange

    # pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_positions())
    # pprint(exchange.fetch_open_orders())
    # pprint(exchange.fetch_my_trades())
    # pprint(exchange.fetch_positions())
    # pprint(exchange.fetch_markets())

    print('sending order')
    result = exchange.create_order(
        'BTC/USDT',
        'market',
        'buy',
        10000,
        None,
        {
            'stopPrice': None,
            'timeInForce': None,
            'reduceOnly': True,
            'trigger': None,
            'closeOnTrigger': False,
            'basePrice': None
        })
    print('got result', result)
    # print('sending order 2')
    # result = exchange.create_order(
    #     'BTC/USDT',
    #     'market',
    #     'buy',
    #     10000,
    #     None,
    #     {
    #         'stopPrice': None,
    #         'timeInForce': None,
    #         'reduceOnly': None,
    #         'trigger': None,
    #         'closeOnTrigger': False,
    #         'basePrice': None
    #     })
    # print('got result 2', result)
    # result = exchange.create_order(
    #     'BTC/USD',
    #     'limit',
    #     'buy',
    #     1,
    #     55000,
    #     {
    #         'stopPrice': None,
    #         'timeInForce': 'GTC',
    #         'reduceOnly': None,
    #         'trigger': 'Mark',
    #         'closeOnTrigger': False,
    #         'basePrice': None
    #     })
    #
    # result = exchange.create_order(
    #     'BTC/USDT',
    #     'limit',
    #     'buy',
    #     0.001,
    #     45000,
    #     {
    #         'stopPrice': None,
    #         'timeInForce': 'GTC',
    #         'reduceOnly': None,
    #         'closeOnTrigger': None,
    #         'basePrice': None,
    #         'trigger': None,
    #     })
    #
    # exchange.cancel_order('18748454326', 'BTC/USD', params={'type': 'limit'})
    # pprint(exchange.cancel_all_orders('BTC/USD'))
# BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX BITMEX #

# BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT #
def test_bybit():
    # exchange = test.mn_bybit_inverse_exchange
    # exchange = test.mn_bybit_linear_exchange
    # exchange = test.tn_bybit_inverse_exchange
    exchange = test.tn_bybit_linear_exchange

    symbol = 'BTC/USDT'
    # symbol = 'BTC/USDT'
    ticker = exchange.fetch_ticker(symbol)
    last = ticker['last']

    # orders = exchange.fetch_orders(symbol)

    # leverageResponse = exchange.switch_isolated(symbol, False, 10, 20)
    leverageResponse = exchange.set_leverage(symbol, 12, 12)

    # exchange.create_order(symbol,
    #                       'stop',
    #                       'sell',
    #                       0.001,
    #                       51001,
    #                       {
    #                           'stopPrice': 51000,
    #                           'timeInForce': 'PO',
    #                           'reduceOnly': None,
    #                           'trigger': 'Last',
    #                           'closeOnTrigger': False,
    #                           'basePrice': last
    #                       })
    # # exchange.create_order(symbol,
    # 'stoplimit',
    # 'buy',
    # 1,
    # last * 0.94,
    # {
    #     'stopPrice': last * 1.06,
    #     'timeInForce': 'PO',
    #     'reduceOnly': None,
    #     'trigger': 'Last',
    #     'closeOnTrigger': False,
    #     'basePrice': last
    # })
    # pprint(exchange.fetch_open_orders('BTC/USDT'))
    pprint(exchange.fetch_open_orders('BTC/USDT'))
    # pprint(exchange.fetch_positions())
    # pprint(exchange.cancel_all_orders('BTC/USD'))
# BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT BYBIT #

# FTX FTX FTX FTX FTX FTX FTX FTX FTX FTX #
def test_ftx():
    exchange = test.mn_ftx_exchange

    pprint(exchange.fetch_open_orders('BTC-PERP', None, None, { 'type': 'stop'}))
    # pprint(exchange.fetch_positions())
    # pprint(exchange.api_referral_success())
# FTX FTX FTX FTX FTX FTX FTX FTX FTX FTX #

# KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN #
def test_kucoin():
    # exchange = test.mn_kucoin_exchange
    exchange = test.tn_kucoin_exchange

    pprint(exchange.fetch_balance())
# KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN KUCOIN #

# PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX #
def test_phemex():
    # exchange = test.mn_phemex_exchange
    exchange = test.mn_phemex_exchange

    pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_markets())
# PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX PHEMEX #

# OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX #
def test_okex():
    # exchange = test.mn_okex_exchange
    exchange = test.tn_okex_exchange
    # result = exchange.create_order(
    #     'BTC-USD-SWAP',
    #     'limit',
    #     'buy',
    #     1,
    #     35000,
    #     {
    #         'stopPrice': None,
    #         'timeInForce': 'GTC',
    #         'reduceOnly': None,
    #         'closeOnTrigger': None,
    #         'basePrice': None,
    #         'trigger': None,
    #     })
    # pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_positions())
    # pprint(exchange.fetch_markets())
# OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX OKEX #

def main():
    # test_binance()
    # test_bitmex()
    # test_bybit()
    # test_ftx()
    # test_kucoin()
    # test_phemex()
    # test_okex()
    # buy_stuff()
    test_kucoin()

if __name__ == "__main__":
    main()

# def main():
#     # test_exchange_get_methods(bybitExchange)
#     # test_exchange_get_methods(bitmexExchange)
#     # test_exchange_get_methods(bybitExchange)
#     # test_exchange_get_methods(binanceExchange)
#     # test_exchange_get_methods(phemexExchange)
#     # test_exchange_get_methods(test.tn_bybit_linear_exchange)
#     test_bybit()
#     test_ftx()


# def test_exchange_get_methods(exchange):
#     print(exchange.name)
#     # pprint(exchange.fetch_positions())
#     pprint(exchange.api_referral_success())

    # pprint(exchange.cancel_all_orders('BTC/USDT'))

    # result = exchange.create_order(
    #     'BTC/USD',
    #     'limit',
    #     'buy',
    #     1,
    #     55000,
    #     {
    #         'stopPrice': None,
    #         'timeInForce': 'GTC',
    #         'reduceOnly': None,
    #         'trigger': 'Mark',
    #         'closeOnTrigger': False,
    #         'basePrice': None
    #     })
    #
    # # exchange.cancel_order('18748454326', 'BTC/USD', params={'type': 'limit'})
    # exchange.fetch_order('342273454577688576', 'BTC-USD-SWAP', params={'type': 'stop'})
    #
    # orders = [{'id': '18747457675', 'type': 'stop'}, {'id': '18747460710', 'type': 'stop'}, {'id': '18747461436', 'type': 'stop'}, {'id': '18747462096', 'type': 'stop'}, {'id': '18747462701', 'type': 'stop'}, {'id': '18747463265', 'type': 'stop'}, {'id': '18747463947', 'type': 'stop'}, {'id': '18747468725', 'type': 'stop'}]
    #
    # for order in orders:
    #
    #     order_before = exchange.fetch_order(order['id'], 'BTC/USD')
    #     print('ORDER BEFORE')
    #     pprint(order_before)
    #     print('ORDER BEFORE')

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

    # cancel_result = exchange.cancel_order(order['id'], 'BTC/USD')
    # print('CANCEL RESULT')
    # pprint(cancel_result)
    # print('CANCEL RESULT')
    #
    # order_after = exchange.fetch_order(order['id'], 'BTC/USD')
    # print('ORDER AFTER')
    # pprint(order_after)
    # print('ORDER AFTER')
    #
    # hi = True

    # print('##########\nfetch_balance\n##########')
    # pprint(exchange.fetch_markets())
    # pprint(exchange.fetch_balance())
    # pprint(exchange.fetch_open_orders())
    # pprint(exchange.fetch_open_orders(params={'type': 'oco'}))
    # print('##########\nfetch_positions\n##########')
    # pprint(exchange.fetch_open_orders('BTC/USD'))
    # pprint(exchange.cancel_order('61b45fad-0b82-4ea2-ac82-4649cfec6862', 'BTCUSDZ21', {'type': 'stop'}))
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000, params={'stopPrice': None, 'timeInForce': 'PO', 'reduceOnly': True, 'trigger': None, 'closeOnTrigger': None})
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000)
    # exchange.create_order('BTC/USD', 'limit', 'buy', 1, 36000, params={ 'timeInForce': 'PO', 'reduceOnly': True, 'trigger': None, 'closeOnTrigger': None})
    # print(exchange.fetch_positions(None, {'currency': 'BTC'})) # phemex - make ts call that calls all
    # pprint(exchange.fetch_positions(None, {'type': 'all'})) # bybit
    # pprint(exchange.fetch_positions())
    # print('##########\nfetch_orders\n##########')
    # pprint(exchange.fetch_orders())
    # pprint(exchange.fetch_open_orders('BTC/USD', None, None)) # phemex /  bybit
    # pprint(exchange.fetch_orders()) # phemex /  bybit
    # pprint(exchange.fetch_open_orders())
    # print('##########\nfetch_my_trades\n##########')
    # pprint(exchange.fetch_my_trades())
    # print(exchange.fetch_my_trades('BTC/USD', None, None))


#
#
# # fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
# ftxExchange = ccxt.ftx({
#     'apiKey': os.environ.get('ftx_key'),
#     'secret': os.environ.get('ftx_secret'),
#     'headers': {
#         'FTX-SUBACCOUNT': 'APITEST',
#     },
#     'enableRateLimit': True,
# })
#
# ftxExchange.fetch_currencies()
#
# # fetch_balance [x], fetch_positions [x], fetch_orders [x] (fees not implemented, but fetch_trades has fees), fetch_my_trades [x] ('side' doesnt show for funding trades)
# bitmexExchange = ccxt.bitmex({
#     'apiKey': os.environ.get('bitmex_key'),
#     'secret': os.environ.get('bitmex_secret'),
#     'enableRateLimit': True,
# })
# # for bitmex testnet https://github.com/ccxt/ccxt/issues/5717
# bitmexExchange.urls['api'] = bitmexExchange.urls['test']
#
# fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
# bybitExchange = ccxt.bybitinverse({
#     'apiKey': os.environ.get('bybit_kjs_key'),
#     'secret': os.environ.get('bybit_kjs_secret'),
#     'enableRateLimit': True
# })
# bybitExchange.set_sandbox_mode(True)
#
# # fetch_balance [ ], fetch_positions [ ], fetch_orders [ ], fetch_my_trades [ ]
# binanceExchange = ccxt.binanceusdm({
#     'apiKey': os.environ.get('binance_key'),
#     'secret': os.environ.get('binance_secret'),
#     'enableRateLimit': True,
#     # 'options': {
#     #      'defaultType': 'future', # USD-M
#     #     #'defaultType': 'delivery', # COIN-M
#     #     #'defaultType': 'spot', # COIN-M
#     #     'leverageBrackets': None,
#     # },
# })
#
# # fetch_balance [x], fetch_positions [x], fetch_orders [x], fetch_my_trades [x]
# phemexExchange = ccxt.phemex({
#     'apiKey': os.environ.get('phemex_key_main'),
#     'secret': os.environ.get('phemex_secret_main'),
#     'enableRateLimit': True,
# })
# # phemexExchange.urls['api'] = phemexExchange.urls['test']
#
# okexExchange = ccxt.okex({
#     'apiKey': os.environ.get('okex_key'),
#     'secret': os.environ.get('okex_secret'),
#     'password': os.environ.get('okex_password'),
#     'enableRateLimit': True,
#     'headers': {
#         'x-simulated-trading': '1',
#     },
# })
# okexExchange.set_sandbox_mode(True)