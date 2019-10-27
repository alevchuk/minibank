## Build Bitcoind (a.k.a. Bitcoin Core)

With unix account that has sudo, install dependencies:
```
sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils  libboost-dev libboost-system-dev libboost-filesystem-dev  libboost-chrono-dev libboost-program-options-dev  libboost-test-dev libboost-thread-dev  libminiupnpc-dev  libzmq3-dev 

sudo apt-get install git
```

At this point change to unix account that will be running bitcoin, e.g.:
```
sudo su -l bitcoin
```

Checkout source code:
```
git clone https://github.com/bitcoin/bitcoin.git ~/src/bitcoin
cd ~/src/bitcoin
git checkout v0.18.0
```
The reason we need to check out the 0.18 tag, is because there is an RPC change in bitocoin 0.19 which is incompatible with LND, until this issue is fixed https://github.com/lightningnetwork/lnd/issues/2961

Prepare for build (one time setup):
```
cd ~/src/bitcoin
./autogen.sh
./configure  --with-gui=no --disable-wallet --disable-tests --prefix=$HOME/bin 
```
> - For ARM achitectures, in some cases you might need to add `--with-boost-libdir=/usr/lib/arm-linux-gnueabihf` 
> - The final output of `configure` should include:   "with zmq  = yes"


Build and Install:
```
make && make install
```

# Upgrade
```
cd ~/src/bitcoin
git pull
make clean && make && make install
```
