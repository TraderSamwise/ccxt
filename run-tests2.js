const fs = require ('fs')
  , log = require ('ololog').handleNodeErrors ()
  // eslint-disable-next-line import/no-dynamic-require, no-path-concat
  , ccxt = require (__dirname);


(async () => {
    const exchange = new ccxt.bitmex({ enableRateLimit: true });
    while (true) {
        const res = await exchange.fetchOHLCV("BNB/USDT", "1m", Date.now() - 1000 * 60 * 60);
        console.log(res)

    }
}) ();



