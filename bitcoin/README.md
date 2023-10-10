## Build Bitcoind (a.k.a. Bitcoin Core)

This manual documents how to build and run Bitcoin on Pi 4.

For using Bitcoin Core as a wallet (e.g. via Specter Desktop), doing what some core devs do https://twitter.com/orionwl/status/1340037662577741830 and install a modern version of berkeleydb (like this `sudo apt install libdb5.3++-dev`) and add `--with-incompatible-bdb` to the `./configure` command

Prerequisites:
 * Pi with a 64-bit OS
 * Login in as unix account that has sudo

## Create bitcoin user

```
sudo adduser --disabled-password bitcoin
```

## Create directories

Make directories inside the data mount point:
```
sudo mkdir /mnt/btrfs/bitcoin
sudo mkdir /mnt/btrfs/bitcoin/src
sudo mkdir /mnt/btrfs/bitcoin/bin

sudo chown -R bitcoin /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin
```

# Bitcoin Cookie

Make shared directory for bitcoin clients (e.g. LND) to be able to read the `.cookie` file:

```
sudo groupadd bitcoinclinets
sudo mkdir /home/bitcoin/bitcoinclients
sudo chmod o=,g=rx,u=rwx /home/bitcoin/bitcoinclients  # others nothing, group read, bitcoin read+write
sudo chmod +s /home/bitcoin/bitcoinclients  # in case subdirectories are made, caryover the permissions
sudo chown bitcoin /home/bitcoin/bitcoinclients
sudo chgrp bitcoinclinets /home/bitcoin/bitcoinclients
```

When bitcoin starts it will make the cookies files restricted to only bitcoin user:
```
ls -l bitcoinclients/
total 8
-rw------- 1 bitcoin bitcoinclinets   75 Jun  2 14:14 cookie
```

To let other account such as LND and Electrs access to the cookie, the workaround is to make a cron job so that the permission changes to this:

```
ls -l bitcoinclients/
total 8
-rw-r----- 1 bitcoin bitcoinclinets   75 Jun  2 14:14 cookie
```

To get that, run:
```
sudo su -l bitcoin
crontab -e
```
and add the following line on the bottom:
```
* *  * * * chmod g+r /home/bitcoin/bitcoinclients/cookie
```

This will make the file accessible to members of `bitcoinclients` group within 1 minute of `bitcoind` writing the file (it writes it during `bitcoind` startup).


# Install needed packages
```
sudo apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils  libboost-dev libboost-system-dev libboost-filesystem-dev  libboost-chrono-dev libboost-program-options-dev  libboost-test-dev libboost-thread-dev  libminiupnpc-dev  libzmq3-dev libdb5.3++-dev
```


# Setup, git clone, and build

Login as bitcoin user and drop into 64-bin environment:
```
sudo su -l bitcoin
```

Make symlinks back to data mount point
```
ln -s /mnt/btrfs/bitcoin/bin ~/bin
ln -s /mnt/btrfs/bitcoin/src ~/src
ln -s /mnt/btrfs/bitcoin/dot-bitcoin-data ~/.bitcoin

echo 'export PATH=$HOME/bin/bin:$PATH  # bitcoind is here' >> ~/.profile
. ~/.profile
```


Checkout source code:
```
git clone https://github.com/bitcoin/bitcoin.git ~/src/bitcoin
cd ~/src/bitcoin
git checkout v25.0  # or find the latest tag with git tag | grep v25
```

if you have bitcoin on v0.23 or lower and LND is 0.15.99 or newer, then LND will fail to start and give the following error 
> error creating wallet config: unable to create partial chain control: node backend does not support taproot

Prepare for build (one time setup):
```
./autogen.sh
./configure  --with-gui=no --disable-tests --with-incompatible-bdb --prefix=$HOME/bin 
```
> - The final output of `configure` should include:   "with zmq  = yes"

Build and Install:
```
make clean && make && make install
```

# Configure and run

For configuring and running bitcoin see "Start Bitcoin" section on the main page https://github.com/alevchuk/minibank/blob/first/README.md#start-bitcoind

# Upgrade
```
cd ~/src/bitcoin
git pull
make clean && make && make install
```
