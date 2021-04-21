### Setup LND environment

1. Add new unix user account "lightning" and setup storge directories on BTRFS

```
sudo adduser --disabled-password lightning

sudo mkdir /mnt/btrfs/lightning
sudo mkdir /mnt/btrfs/lightning/lnd-data
sudo mkdir /mnt/btrfs/lightning/gocode
sudo mkdir /mnt/btrfs/lightning/lnd-e2e-testing
sudo mkdir /mnt/btrfs/lightning/src

sudo chown -R lightning /mnt/btrfs/lightning
```

2. Log-in as "lightning" user and setup symlinks


```
sudo su -l lightning

ln -s /mnt/btrfs/lightning/lnd-data ~/.lnd
ln -s /mnt/btrfs/lightning/gocode
ln -s /mnt/btrfs/lightning/lnd-e2e-testing
ln -s /mnt/btrfs/lightning/src
```



### Install Tor

```
sudo apt install tor
```

 * Minibank needs tor version **0.3.3.6** or above. Fortunaly Rasiban 10 already has that. On older distos [build tor from source](https://github.com/alevchuk/minibank/tree/first/tor#build-from-source). 
 * Minibank uses Tor for LND. Yet not for Bitcoin sync traffic because that seems to introduce delays.

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


### Build Go
Follow instrutions under [alevchuk/minibank/go](https://github.com/alevchuk/minibank/blob/first/go/)


### Build LND

1. Install dependencies:
* Fun fact: build-essential contains `make`
```
sudo apt-get install build-essential
```

2. Log in as "lightning"
```
sudo su -l lightning
```

3. Download, build, and Install LND:
```
go get -d github.com/lightningnetwork/lnd
(cd $GOPATH/src/github.com/lightningnetwork/lnd && make clean && make && make install)
```
