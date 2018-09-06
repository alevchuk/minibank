# Litecoin

Testnet on Bitcoin is having issues (hight fees), so I'm switching to testing LND with Litecoin.

LND supports two implementations of Litcoin full node: 
1. **litecoind**
2. **ltcd**

litecoind is the official implementation, yet
currently I'm using ltcd because litecoind has an issue when starting up: https://github.com/lightningnetwork/lnd/issues/1854
