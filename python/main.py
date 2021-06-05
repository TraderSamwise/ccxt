import os
from pprint import pprint

import ccxt

# Bitmex
# Bybit
# Binance
# FTX
# Phemex

exchange = ccxt.ftx({
    'apiKey': os.environ.get('ftx_key'),
    'secret': os.environ.get('ftx_secret'),
    'enableRateLimit': True
})


def main():
    print("BITMEX")
    res = exchange.fetch_positions()
    pprint(res)
    # print("=============")
    # print("BYBIT")
    # res_bybit = exchange_bybit.fetch_positions()
    # pprint(res_bybit[0])
    # print("=============")
    # print("THIS EXCHANGE")
    # res = exchange.fetch_positions()
    # pprint(res[0])

if __name__ == "__main__":
    main()