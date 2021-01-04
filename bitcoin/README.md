## Build Bitcoind (a.k.a. Bitcoin Core)

With unix account that has sudo, install dependencies:
```
sudo apt install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils  libboost-dev libboost-system-dev libboost-filesystem-dev  libboost-chrono-dev libboost-program-options-dev  libboost-test-dev libboost-thread-dev  libminiupnpc-dev  libzmq3-dev 

sudo apt install git
```

At this point change to unix account that will be running bitcoin, e.g.:
```
sudo su -l bitcoin
```

Checkout source code:
```
git clone https://github.com/bitcoin/bitcoin.git ~/src/bitcoin
cd ~/src/bitcoin
git checkout v0.18.1
```
The reason we need to check out the 0.18 tag, is because there is an RPC change in bitocoin 0.19 which is incompatible with LND, until this issue is fixed https://github.com/lightningnetwork/lnd/issues/2961

Prepare for build (one time setup):
```
cd ~/src/bitcoin
./autogen.sh
./configure  --with-gui=no --disable-wallet --disable-tests --prefix=$HOME/bin 
```
> - The final output of `configure` should include:   "with zmq  = yes"
> - For using Bitcoin Core as a wallet (e.g. via Specter Desktop), follow what some core devs do https://twitter.com/orionwl/status/1340037662577741830 and install a modern version of berkeleydb (like this `sudo apt install libdb5.3++-dev`) and add `--with-incompatible-bdb` to the `./configure` command

Build and Install:
```
make clean && make && make install
```

# Upgrade
```
cd ~/src/bitcoin
git pull
make clean && make && make install
```
