# bankminus
bitcoin lightning node

![alt text](https://raw.githubusercontent.com/alevchuk/bankminus/master/model3_64g.jpg "bankminus model 3, 64GB microSD cards, running testnet LND")

## Hardware

### All Models

* 2x Micro SD cards https://camelcamelcamel.com/Sandisk-Ultra-200GB-Micro-Adapter/product/B073JY5T7T 

### Model 1

* Pi 3 B+ https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW
* Touchscreen https://camelcamelcamel.com/Raspberry-Pi-7-Touchscreen-Display/product/B0153R2A9I
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Case https://camelcamelcamel.com/Case-Official-Raspberry-Touchscreen-Display/product/B01HV97F64

### Model 2 [Discontinued]

* Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* USB cable https://camelcamelcamel.com/UGREEN-Adapter-Samsung-Controller-Smartphone/product/B00LN3LQKQ
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Touchscreen ? https://camelcamelcamel.com/LANDZO-Touch-Screen-320480-Raspberry/product/B01IGBDT02
* Case ?

### Model 3

* 2x Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* 2x Case with USB-A Addon Board https://camelcamelcamel.com/MakerFocus-Raspberry-Required-Connector-Protective/product/B07BK2BR6C
* Power Supply https://camelcamelcamel.com/Tranesca-charger-foldable-Samsung-More-Black/product/B01385COIE

## Operating System

Raspbian Stretch Lite https://www.raspberrypi.org/downloads/raspbian/

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

## Network

## Build Tor

## Start Tor

## Build Bitcoind

## Start Bitcoind

## Build LND

## Start LND

## Touchscreen

## systemd


