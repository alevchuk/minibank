## Build Bitcoind (a.k.a. Bitcoin Core)

With unix account that has sudo, install dependencies:
```
sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils 
sudo apt-get install libboost-dev libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev 
sudo apt-get install libminiupnpc-dev 
sudo apt-get install libzmq3-dev 
```

At this point change to unix account that will be running bitcoin, e.g.:
```
sudo su -l bitcoin
```

Checkout source code:
```
git clone https://github.com/bitcoin/bitcoin.git ~/src/bitcoin
```

Prepare for build (one time setup):
```
cd ~/src_github.com/bitcoin
./autogen.sh
./configure  --with-gui=no --disable-wallet --disable-tests --prefix=$HOME/bin
```

Build and Install:
```
make && make install
```

# Upgrade
```
cd ~/src_github.com/bitcoin
git pull
make clean && make && make install
```
