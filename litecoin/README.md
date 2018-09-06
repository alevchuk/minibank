# Litecoin

Testnet on Bitcoin is having issues (hight fees), so I'm switching to testing LND with Litecoin.

Also it will be easier to get bootstrapped on Litecoin mainnet because the fees are ~0.10 USD per transaction and chain size is 10x smaller (currently 18.95 GB on Litecoin vs 213.10 GB on Bitcoin).

LND supports two implementations of Litcoin full node: 
1. **litecoind**
2. **ltcd**

Currently I'm using ltcd because it's easier to build and litecoind has an issue when starting up: https://github.com/lightningnetwork/lnd/issues/1854
