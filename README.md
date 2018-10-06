# bankminus
bitcoin lightning node

![alt text](https://raw.githubusercontent.com/alevchuk/bankminus/master/model3_64g.jpg "bankminus model 3, 64GB microSD cards, running testnet LND")

Table of contents
=================

  * [Hardware](#hardware)
  * [Network](#network)
  * [Storage](#storage)
  * [Build Go](#build-go)
  * [Build LND](#build-lnd)
  * [Start LND](#start-lnd)
  * [Monitoring](#monitoring)
 
## Hardware

### All Models

### Model 1 :: Base Station

* Pi 3 B+ https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW
* 2x Micro SD cards https://camelcamelcamel.com/Sandisk-Ultra-200GB-Micro-Adapter/product/B073JY5T7T 
* Touchscreen https://camelcamelcamel.com/Raspberry-Pi-7-Touchscreen-Display/product/B0153R2A9I
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Case https://camelcamelcamel.com/Case-Official-Raspberry-Touchscreen-Display/product/B01HV97F64

### Model 3 :: LND Node

* 2x Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* 2x Micro SD cards https://camelcamelcamel.com/Sandisk-Ultra-200GB-Micro-Adapter/product/B073JY5T7T 
* 2x Case with USB-A Addon Board https://camelcamelcamel.com/MakerFocus-Raspberry-Required-Connector-Protective/product/B07BK2BR6C
* Power Supply https://camelcamelcamel.com/Tranesca-charger-foldable-Samsung-More-Black/product/B01385COIE

## Operating System

Raspbian Stretch Lite https://www.raspberrypi.org/downloads/raspbian/

## Network

Edit `/etc/wpa_supplicant/wpa_supplicant.conf`

Add WiFi network name and password:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

For troubleshooting see:
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

## Memory

Pi Zero W has 433 MB of usable RAM. Additional memory needs to be added as swap.

Edit `/etc/dphys-swapfile`
```
CONF_SWAPSIZE=600
CONF_MAXSWAP=600
```

Test:
```
sudo dphys-swapfile swapoff
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

A note on microSD card wear and tear from Swap: 

I have been running Bitcoind + LND on this setup for over 6 months on two Pi Zero W boards and still have not seen failures related to swap wearing out the microSD cards. For context on why this is important, see "System with too little RAM" section in [https://askubuntu.com/a/652355/5191]. When failur or slow-downs happen due to micro SD card lifespan, a quick remediation would be to swap the primary and the backup sd cards as described in the Storage section.

## Storage

### Partition

```
sudo parted /dev/mmcblk0
```

* First partition is boot
* Second partition is for operating system
* Third partition is for software and data

Allocate 5GB to Second and the rest to Thrid.

Results should look like this:
```
Model: SD GC2QT (sd/mmc)
Disk /dev/mmcblk0: 200.0GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      4194kB  49.5MB  45.3MB  primary  fat32        lba
 2      50.3MB  5500MB  5450MB  primary  ext4
 3      5450MB  200.0GB 194.5GB primary  btrfs
```


### iSCSI

(Not needed for Base Station beacause it uses an external USB Card reader)

iSCSI makes a storage device available over the network. This is useful to avoid cables, USB, and extra card readers.


### BTRFS 

RAID-1

## Build Bitcoind

## Start Bitcoind

## Build Go

This section is based on https://golang.org/doc/install/source and https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#build-go

Prerequisits:
* Raspbian GNU/Linux 9
* Create unix account "lnd"

1. Fetch bootstrap go (as root)

```
sudo apt-get install golang-1.6
sudo apt-get install git
```

2. Log-in as "lnd"

```
sudo su -l lnd
```

--- after this all commands should be run under the "lnd" account ---

3. Set bootstrap path and gopath. To ~lightning/.profile add:

```
export GOROOT_BOOTSTRAP=/usr/lib/go-1.6

export GOROOT=~/src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
```

4. Fetch new go
```
mkdir ~/src
cd ~/src
git clone https://go.googlesource.com/go
cd go
git fetch
git checkout go1.11.1
```

5. Build new go
```
. ~/.profile
cd $GOROOT/src
./make.bash
```
At the end it should say "Installed commands in $GOROOT/bin"



## Build LND

## Start LND

## Monitoring

https://github.com/prometheus/prometheus#building-from-source

## systemd


