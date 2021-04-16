## Build Bitcoind (a.k.a. Bitcoin Core)


This manual documents how to build and run Bitcoin on Pi 4. The main challenge is that latest (after 0.19) versions of Bitcoin requires a 64-bit environment while Pi base operating system Rasbian is 32-bit. Fortunately Pi 4 hardware is 64-bit.

Prerequisites:
 * Boot Pi in [64-bit mode](https://medium.com/for-linux-users/how-to-make-your-raspberry-pi-4-faster-with-a-64-bit-kernel-77028c47d653) 
 * Login in as unix account that has sudo


## Chroot for 64-bit environment

```
sudo adduser --disabled-password bitcoin
sudo apt install -y debootstrap schroot

cat << EOF | sudo tee /etc/schroot/chroot.d/pi64
[pi64]
description=builds that need 64-bit environment
type=directory
directory=/mnt/btrfs/pi64
users=grafana
root-groups=root
profile=desktop
personality=linux
preserve-environment=true
EOF

sudo debootstrap --arch arm64 buster /mnt/btrfs/bitcoin64

sudo schroot -c bitcoin64 -- apt update
sudo schroot -c bitcoin64 -- apt upgrade -y

sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin
sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin/src
sudo mkdir /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin/bin

sudo chown -R bitcoin /mnt/btrfs/bitcoin64/mnt/btrfs/bitcoin
```



# Install needed packages
```
sudo schroot -c bitcoin64 -- apt install -y python3.7 python3-distutils g++ make golang git python2
```


# Change user
Login as bitcoin user and drop into 64-bin environment:
```
sudo su -l bitcoin
schroot -c pi64
```

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
git checkout v0.19.1
```

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
