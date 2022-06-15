import asyncio
from pprint import pprint

import test_exchanges as test
from ccxt.async_support.kucoinfutures import kucoinfutures


async def test_kucoin():
    # exchange = test.mn_binance_usdm_exchange
    exchange: kucoinfutures = test.mn_kucoin_exchange_pro
    await exchange.load_markets()
    pprint(exchange.markets)
    '''
    # symbol = 'BTC/USDT'
    symbol = 'BTC/USD'
    ticker = await exchange.fetch_ticker(symbol)
    last = ticker['last']
    '''



def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_kucoin())
    test_kucoin()


if __name__ == "__main__":
    main()
