const fs = require ('fs')
  , log = require ('ololog').handleNodeErrors ()
  // eslint-disable-next-line import/no-dynamic-require, no-path-concat
  , ccxt = require (__dirname);


(async () => {
    const exchange = new ccxt.ftx ({ enableRateLimit: true });
    while (true) {
        await exchange.loadMarkets()
        console.log(exchange.currencies.USD)

    }
}) ();



