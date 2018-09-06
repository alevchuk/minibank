# Litecoind

# Update: 2019-09-06

Cancelling my LTC attempt... See [README.md](README.md)

# Archive before 2019-09-06

## Build Litecoind

Install dependencies:
```
sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils 
sudo apt-get install libboost-dev libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev 
sudo apt-get install libminiupnpc-dev 
sudo apt-get install libzmq3-dev 
```

Checkout source code:
```
mkdir ~/src_github.com
cd ~/src_github.com
git clone https://github.com/litecoin-project/litecoin.git
```

Build:
```
cd ~/src_github.com/litecoin
./autogen.sh
./configure  --with-gui=no --disable-wallet --disable-tests --prefix=$HOME/bin
```

```
make
make install
```
