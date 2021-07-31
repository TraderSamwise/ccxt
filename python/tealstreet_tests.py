import os
from pprint import pprint
import ccxt
import pytest

__test__ = True

# exchanges

ftxExchange = ccxt.ftx({
    'apiKey': os.environ.get('ftx_key'),
    'secret': os.environ.get('ftx_secret'),
    'headers': {
        'FTX-SUBACCOUNT': 'APITEST',
    },
    'enableRateLimit': True,
})

bitmexExchange = ccxt.bitmex({
    'apiKey': os.environ.get('bitmex_key'),
    'secret': os.environ.get('bitmex_secret'),
    'enableRateLimit': True,
})
bitmexExchange.set_sandbox_mode(True)

bybitExchange = ccxt.bybit({
    'apiKey': os.environ.get('bybit_key'),
    'secret': os.environ.get('bybit_secret'),
    'enableRateLimit': True,
})
bybitExchange.set_sandbox_mode(True)

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

# start test stuff

# SETTINGS
exchange = bybitExchange
symbol = 'BTC/USD'
size = 1
ticker = exchange.fetch_ticker(symbol)
last = ticker['last']
# /SETTINGS
orders = []
actions = []

def get_close_on_trigger_value(result):
    keys = ['close_on_trigger']
    for key in keys:
        if key in result:
            return exchange.safe_value(result, key)
    return None

def get_info_trigger_value(result):
    keys = ['trigger', 'trigger_by', 'execInst']
    for key in keys:
        if key in result:
            return exchange.safe_value(result, key)
    return None

def do_create_order(args):
    print('create_order(', *args, ')')
    result = exchange.create_order(*args)
    print('Result:')
    pprint(result)
    print('༼ つ ◕_◕ ༽つ')
    return result

def test_market_buy_not_post_only():
    print(exchange.name)
    print('Market buy, post only = false.')
    result = do_create_order([
        symbol,
        'market',
        'buy',
        size*5,
        None,
        {
            'stopPrice': None,
            'timeInForce': 'GTC', # GTC, PO
            'reduceOnly': False,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'closed' and order['postOnly'] == False

def test_market_sell_not_post_only():
    print(exchange.name)
    print('Market sell, post only = false.')
    result = do_create_order([
        symbol,
        'market',
        'sell',
        size,
        None,
        {
            'stopPrice': None,
            'timeInForce': 'GTC', # GTC, PO
            'reduceOnly': False,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'closed' and order['postOnly'] == False

def test_limit_buy_below_last_post_only_reduce_only():
    print('Limit buy below last, reduce only = true and post only = true. Should not post.')
    try:
        result = do_create_order([
            symbol,
            'limit',
            'buy',
            size,
            last * 0.99,
            {
                'stopPrice': None,
                'timeInForce': 'PO',  # GTC, PO
                'reduceOnly': True,
                'trigger': None,
                'closeOnTrigger': None,
                'basePrice': None
            }
        ])
        orders.append({'id': result['id'], 'type': 'limit'})
        assert False
    except:
        assert True

def test_limit_buy_below_last_not_post_only_not_reduce_only():
    print('Limit buy below last, reduce only = false and post only = false.')
    result = do_create_order([
        symbol,
        'limit',
        'buy',
        size,
        last * 0.98,
        {
            'stopPrice': None,
            'timeInForce': 'GTC',  # GTC, PO
            'reduceOnly': False,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    orders.append({'id': result['id'], 'type': 'limit'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and order['postOnly'] == False

def test_limit_sell_below_last_post_only_reduce_only():
    print('Limit sell above last, reduce only = true and post only = true.')
    result = do_create_order([
        symbol,
        'limit',
        'sell',
        size,
        last * 1.01,
        {
            'stopPrice': None,
            'timeInForce': 'PO', # GTC, PO
            'reduceOnly': True,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    orders.append({'id': result['id'], 'type': 'limit'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and order['postOnly'] == True # TODO: reduce only

def test_limit_sell_above_last_not_post_only_not_reduce_only():
    print('Limit sell above last, reduce only = false and post only = false.')
    result = do_create_order([
        symbol,
        'limit',
        'sell',
        size,
        last * 1.02,
        {
            'stopPrice': None,
            'timeInForce': 'GTC',  # GTC, PO
            'reduceOnly': False,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    orders.append({'id': result['id'], 'type': 'limit'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and  order['postOnly'] == False

def test_stop_market_sell_below_last_close_on_trigger():
    print('Market sell stop below last. Close on trigger = true.')
    result = do_create_order([
       symbol,
       'stop',
       'sell',
       size,
       None,
       {
          'stopPrice':last * 0.97,
          'timeInForce':'GTC',
          'reduceOnly':None,
          'trigger':'Last',
          'closeOnTrigger':True,
          'basePrice': last
       }
    ])
    orders.append({'id': result['id'], 'type': 'limit'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_market_sell_below_last():
    print('Market sell stop below last. Close on trigger = false.')
    result = do_create_order([
        symbol,
        'stop',
        'sell',
        size,
        None,
        {
            'stopPrice': last * 0.96,
            'timeInForce': 'GTC',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice':  last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == False or get_close_on_trigger_value(result['info']) == None)

def test_stop_market_sell_above_last(): # TODO: bitmex is filling on this
    print('Market sell stop above last. Close on trigger = false.')
    result = do_create_order([
        symbol,
        'stop',
        'sell',
        size,
        None,
        {
            'stopPrice': last * 1.03,
            'timeInForce': 'GTC',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == False or get_close_on_trigger_value(result['info']) == None)

def test_stop_market_buy_above_last_close_on_trigger():
    print('Market buy stop above last. Close on trigger = true.')
    result = do_create_order([
       symbol,
       'stop',
       'buy',
       size,
       None,
       {
          'stopPrice':last * 1.04,
          'timeInForce':'GTC',
          'reduceOnly':None,
          'trigger':'Last',
          'closeOnTrigger':True,
          'basePrice': last
       }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_market_buy_above_last():
    print('Market buy stop above last. Close on trigger = false.')
    result = do_create_order([
        symbol,
        'stop',
        'buy',
        size,
        None,
        {
            'stopPrice': last * 1.05,
            'timeInForce': 'GTC',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == False or get_close_on_trigger_value(result['info']) == None)

def test_stop_market_buy_below_last(): # TODO: bitmex is filling on this
    print('Market buy stop below last. Close on trigger = false.')
    result = do_create_order([
       symbol,
        'stop',
        'buy',
        size,
        None,
        {
            'stopPrice': last * 0.95,
            'timeInForce': 'GTC',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and (get_close_on_trigger_value(result['info']) == False or get_close_on_trigger_value(result['info']) == None)

def test_stop_limit_buy_above_last():
    print('Limit buy stop above last. Close on trigger = false. Trigger = Last.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'buy',
        size,
        last * 0.94,
        {
            'stopPrice': last * 1.06,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and 'Last' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_limit_buy_above_mark():
    print('Limit buy stop above last. Close on trigger = true. Trigger = Mark.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'buy',
        size,
        last * 0.93,
        {
            'stopPrice': last * 1.07,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Mark',
            'closeOnTrigger': True,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert (order['status'] == 'open') and 'Mark' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_limit_buy_above_index():
    print('Limit buy stop above last. Close on trigger = true. Trigger = Index.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'buy',
        size,
        last * 0.92,
        {
            'stopPrice': last * 1.08,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Index',
            'closeOnTrigger': True,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and 'Index' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_limit_sell_below_last():
    print('Limit sell stop below last. Close on trigger = false. Trigger = Last.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'sell',
        size,
        last * 1.09,
        {
            'stopPrice': last * 0.91,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Last',
            'closeOnTrigger': False,
            'basePrice': last
        }
    ])
    orders.append({'id': result['id'], 'type': 'stop'})
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and 'Last' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_cancel_order():
    print('Cancel a few limit orders.')
    asserts = []
    results = []
    orders_to_cancel = [x for x in orders if x['type'] == 'limit']
    r = 2 if len(orders_to_cancel) >= 2 else orders_to_cancel
    for i in range(r):
        id = orders_to_cancel.pop()['id']
        try:
            order = exchange.fetch_order(id, symbol)
            if (order):
                result = exchange.cancel_order(id, symbol, params={'type': 'limit'})
                results.append(result)
                asserts.append(result['id'] == id)
        except:
            assert False
    pprint(results)
    print('༼ つ ◕_◕ ༽つ')
    assert any(asserts)

def test_cancel_stop_order():
    print('Cancel a few stop orders.')
    asserts = []
    results = []
    orders_to_cancel = [x for x in orders if x['type'] == 'stop']
    r = 5 if len(orders_to_cancel) >= 5 else orders_to_cancel
    for i in range(r):
        id = orders_to_cancel.pop()['id']
        try:
            order = exchange.fetch_order(id, symbol)
            if (order and order['status'] == 'open'):
                result = exchange.cancel_order(id, symbol, params={'type': 'stop'})
                results.append(result)
                asserts.append(result['id'] == id)
        except:
            assert False
    pprint(results)
    print('༼ つ ◕_◕ ༽つ')
    assert any(asserts)

def test_stop_limit_sell_below_mark():
    print('Limit sell stop below mark. Close on trigger = true. Trigger = Mark.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'sell',
        size,
        last * 1.10,
        {
            'stopPrice': last * 0.90,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Mark',
            'closeOnTrigger': True,
            'basePrice': last
        }
    ])
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and 'Mark' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_stop_limit_sell_below_index():
    print('Limit sell stop below last. Close on trigger = true. Trigger = Index.')
    result = do_create_order([
        symbol,
        'stoplimit',
        'sell',
        size,
        last * 1.11,
        {
            'stopPrice': last * 0.89,
            'timeInForce': 'PO',
            'reduceOnly': None,
            'trigger': 'Index',
            'closeOnTrigger': True,
            'basePrice': last
        }
    ])
    order = exchange.fetch_order(result['id'], symbol)
    assert order['status'] == 'open' and 'Index' in get_info_trigger_value(result['info']) and (get_close_on_trigger_value(result['info']) == True or get_close_on_trigger_value(result['info']) == None)

def test_cancel_all_orders():
    print('Cancel all orders.')
    results = []
    results.append(exchange.cancel_all_orders(symbol))
    results.append(exchange.cancel_all_orders(symbol, params={'type': 'stop'}))
    pprint(results)
    print('༼ つ ◕_◕ ༽つ')
    open_orders = exchange.fetch_open_orders(symbol)
    open_orders = [x for x in open_orders if x['status'] != 'open']
    assert not open_orders

def test_close_position():
    print(exchange.name)
    print('Close position')
    result = do_create_order([
        symbol,
        'market',
        'sell',
        size*10,
        None,
        {
            'stopPrice': None,
            'timeInForce': 'GTC',  # GTC, PO
            'reduceOnly': True,
            'trigger': None,
            'closeOnTrigger': None,
            'basePrice': None
        }
    ])
    assert result
