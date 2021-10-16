const fs = require ('fs')
  , log = require ('ololog').handleNodeErrors ()
  // eslint-disable-next-line import/no-dynamic-require, no-path-concat
  , ccxt = require (__dirname);


(async () => {
    const exchange = new ccxt.bybit({ enableRateLimit: true });
    while (true) {
        const res = await exchange.fetchOHLCV("XRP/USD", "1m", Date.now() - 1000*120)
        console.log(res)

    }
}) ();



