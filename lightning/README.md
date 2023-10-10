# Install LND and Tor

This manual documents how to build and run Lightning on Pi 4.

Prerequisites:
 * Boot Pi with a 64-bit OS
 * Login in as Unix account that has sudo

## 1. Create Lightning user

```
sudo adduser --disabled-password lightning
```

## 2. Install Tor

```
sudo apt install tor
```

 * Minibank uses Tor for LND. Yet not for Bitcoin sync traffic because that introduces delays.

1. Edit `/etc/tor/torrc` 
* Uncomment "ControlPort 9051"
2. Run 
```
sudo systemctl restart tor@default.service
```

Add lightning user to be part of the Tor group (e.g. it needs read permissions to /run/tor/control.authcookie )
```
sudo /usr/sbin/adduser lightning debian-tor
```

## 3. Make directories inside the data mount point:
```
sudo mkdir -p /mnt/btrfs/lightning
sudo mkdir    /mnt/btrfs/lightning/src
sudo mkdir    /mnt/btrfs/lightning/bin
sudo mkdir    /mnt/btrfs/lightning/gocode
sudo mkdir    /mnt/btrfs/lightning/lnd-data
sudo mkdir    /mnt/btrfs/lightning/lnd-e2e-testing

sudo chown -R lightning /mnt/btrfs/lightning
```

## 4. Install needed packages

```
sudo apt install -y git build-essential golang
```

Fun facts:
* build-essential contains `make`
* golang is an older version of go that is needed to build modern Go


## 5. Setup LND environment

Log-in as "lightning" user and setup symlinks

```
sudo su -l lightning

ln -s /mnt/btrfs/lightning/lnd-data ~/.lnd
ln -s /mnt/btrfs/lightning/gocode
ln -s /mnt/btrfs/lightning/lnd-e2e-testing
ln -s /mnt/btrfs/lightning/src
```

## 6. Build Go
Follow instructions under [alevchuk/minibank/go](https://github.com/alevchuk/minibank/blob/first/go/)


## 7. Build LND

1. Log in as "lightning"
```
sudo su -l lightning
```

2. Download, build, and Install LND:
```
cd ~/src
git clone https://github.com/lightningnetwork/lnd
cd lnd
git checkout $(git tag | grep v0.16.*-beta$ | sort -V | tail -n1)  # checkout latest minor version

(cd ~/src/lnd && make clean && make install)
```
