import test_exchanges as test


def test_kucoin():
    # exchange = test.mn_binance_usdm_exchange
    exchange = test.mn_kucoin_exchange

    # symbol = 'BTC/USDT'
    symbol = 'BTC/USD'
    ticker = exchange.fetch_ticker(symbol)
    last = ticker['last']

    markets = exchange.fetch_markets()

    print(markets)


def main():
    test_kucoin()


if __name__ == "__main__":
    main()