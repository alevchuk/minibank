## Build Bitcoind (a.k.a. Bitcoin Core)


This manual documents how to build and run Bitcoin on Pi 4. The main challenge is that latest (after 0.19) versions of Bitcoin require a 64-bit environment while Pi base operating system Rasbian is 32-bit. Fortunately Pi 4 hardware is 64-bit.

For using Bitcoin Core as a wallet (e.g. via Specter Desktop), doing what some core devs do https://twitter.com/orionwl/status/1340037662577741830 and install a modern version of berkeleydb (like this `sudo apt install libdb5.3++-dev`) and add `--with-incompatible-bdb` to the `./configure` command

Prerequisites:
 * Boot Pi in [64-bit mode](https://medium.com/for-linux-users/how-to-make-your-raspberry-pi-4-faster-with-a-64-bit-kernel-77028c47d653) 
 * Login in as unix account that has sudo


## Chroot for 64-bit environment

```
sudo adduser --disabled-password bitcoin
sudo apt install -y debootstrap schroot

cat << EOF | sudo tee /etc/schroot/chroot.d/bitcoin64
[bitcoin64]
description=builds that need 64-bit environment
type=directory
directory=/mnt/btrfs/bitcoin64
users=bitcoin
root-groups=root
profile=desktop
personality=linux
preserve-environment=true
EOF

sudo debootstrap --arch arm64 buster /mnt/btrfs/bitcoin64

sudo schroot -c bitcoin64 -- apt update
sudo schroot -c bitcoin64 -- apt upgrade -y
```

Make directories inside the data mount point:
```
sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin
sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin/src
sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin/bin

sudo chown -R bitcoin /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin
```



# Install needed packages
```
sudo schroot -c bitcoin64 -- apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils  libboost-dev libboost-system-dev libboost-filesystem-dev  libboost-chrono-dev libboost-program-options-dev  libboost-test-dev libboost-thread-dev  libminiupnpc-dev  libzmq3-dev libdb5.3++-dev
```


# Setup, git clone, and build

Login as bitcoin user and drop into 64-bin environment:
```
sudo su -l bitcoin
schroot -c bitcoin64
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
git checkout v0.20.1
```

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

# Upgrade
```
cd ~/src/bitcoin
git pull
make clean && make && make install
```
