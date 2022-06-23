import asyncio
from pprint import pprint

import test_exchanges as test
from ccxt.async_support.kucoinfutures import kucoinfutures
# from python_utils.trace_prints import TracePrints
# import sys
# sys.stdout = TracePrints()


async def test_kucoin():
    # exchange = test.mn_binance_usdm_exchange
    exchange: kucoinfutures = test.mn_kucoin_exchange_pro
    await exchange.load_markets()
    # exchange.verbose = True
    balance = await exchange.fetch_balance()
    pprint(balance)
    await exchange.close() # kucoin requires to release all resources with an explicit call to the .close() coroutine
    '''
    # symbol = 'BTC/USDT'
    symbol = 'BTC/USD'
    ticker = await exchange.fetch_ticker(symbol) 
    last = ticker['last']
    '''



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_kucoin())


if __name__ == "__main__":
    main()
