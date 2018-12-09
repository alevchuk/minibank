# minibank
bitcoin lightning node

![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/model3_64g.jpg "minibank model 3, 64GB microSD cards, running testnet LND")

Table of contents
=================

WARNING: (1) This manual is incomplete. (2) The prototype described here is work in progress...

  * [Hardware](#hardware)
  * [Network](#network)
  * [Storage](#storage)
    * [Partitions](#partition)
    * [iSCSI](#iscsi)
    * [BTRFS](#btrfs)
  * [Software](#software)
    * [Build Bitcoin](#build-bitcoind)
    * [Start Bitcoin](#start-bitcoind)
    * [Build Go](#build-go)
    * [Build LND](#build-lnd)
    * [Start LND](#start-lnd)
  * [Monitoring](#monitoring)
    * [Node exporters](#node-exporters)
    * [Prometheus](#prometheus)
    * [Grafana](#grafana)
  * [Service Manager](#service-manager)
 
## Hardware

### Model 1 :: Base Station

* Pi 3 B+ https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW
* 2x Micro SD cards https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q
* Touchscreen https://camelcamelcamel.com/Raspberry-Pi-7-Touchscreen-Display/product/B0153R2A9I
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Case https://camelcamelcamel.com/Case-Official-Raspberry-Touchscreen-Display/product/B01HV97F64

### Model 3 :: LND Node

* 2x Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* 2x Micro SD cards https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q
* 2x Case with USB-A Addon Board https://camelcamelcamel.com/MakerFocus-Raspberry-Required-Connector-Protective/product/B07BK2BR6C
* Power Supply https://camelcamelcamel.com/Tranesca-charger-foldable-Samsung-More-Black/product/B01385COIE

## Operating System

Raspbian Stretch Lite https://www.raspberrypi.org/downloads/raspbian/

## Network

* The changes described in this section need to be applied to all hosts.

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

You'll need two Raspberry Pi Zero W (Model 3) one for LND and the other one for Bitcoind. Optionally, you can get a touchscreen Base Station (Model 1) for monitoring. Monitoring consists of a time-series database and a web user interface. I'll call all of the Pis "hosts" and use the hostnames `l1`, `b1`, and `base` in this manual.

Lookup the IP addresses by running `ip addr` on each node.

Edit `/etc/hosts` and add IP addresses for the 3 node, for example:
```
192.168.0.10    l1
192.168.0.11    b1
192.168.0.12    base
```

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

I have been running Bitcoind + LND on this setup for over 6 months on two Pi Zero W boards and still have not seen failures related to swap wearing out the microSD cards. For context on why this is important, see "System with too little RAM" section in [https://askubuntu.com/a/652355/5191]. When failure or slow-downs happen due to micro SD card lifespan, a quick remediation would be to swap the primary and the backup sd cards as described in the Storage section.

## Storage

### Partition

The two hosts `b1` and `l1` will have identical SD card partition table. 

```
sudo parted /dev/mmcblk0
```

* First partition is boot
* Second partition is for operating system
* Third partition is for Bitcoin software and data
* Fourth partition is for LND software and data

Allocate 5G to **Second**, 10G to **Fourth**, and the rest to Third.

Results should look like this:
```
(parted) p
Model: SD GC2QT (sd/mmc)
Disk /dev/mmcblk0: 64.0GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      4194kB  49.5MB  45.3MB  primary  fat32        lba
 2      50.3MB  4500MB  4450MB  primary  ext4
 3      4500MB  54.0GB  49.5GB  primary  btrfs
 4      54.0GB  64.0GB  10.0GB  primary  btrfs        
```


### iSCSI

(Not needed for Base Station because Base Station will use an external USB Card reader)

iSCSI makes a storage device available over the network. This is useful to avoid cables, USB, and extra card readers.

Notes are based on https://www.tecmint.com/setup-iscsi-target-and-initiator-on-debian-9/ - yet here we avoid using LVM

You'll need to set things like $$PASSWORD1_HERE$$ with unique passwords. Generate random strings (of 30 alphanumeric characters) for each password. 

Part 1: Target

On host b1 setup the following

```
apt-get install tgt
```

Edit
/etc/tgt/conf.d/bankminus_iscsi.conf
```
<target iqn.2018-09.bankminus:btrfs-bitcoind>
     backing-store /dev/mmcblk0p3
     initiator-address 192.168.0.15
     incominguser bankminus-iscsi-user1 $$PASSWORD1_HERE$$
     outgoinguser bankminus-iscsi-target2  $$PASSWORD2_HERE$$
</target>
<target iqn.2018-09.bankminus:btrfs-lnd>
     backing-store /dev/mmcblk0p4
     initiator-address 192.168.0.15
     incominguser bankminus-iscsi-user3 $$PASSWORD3_HERE$$
     outgoinguser bankminus-iscsi-target4  $$PASSWORD4_HERE$$
</target>

```

Restart tgt service:
```
service tgt restart
```

Check exported targets:
```
tgtadm --mode target --op show
```

Check connections (initiator to target) on target
```
tgtadm --mode conn --op show --tid 1
```

Part 2: Initiator

On host b1 mount the remote filesystem


```
apt-get install open-iscsi
```

Restart 
``
service open-iscsi restart
``

Discover targets:
```
iscsiadm  -m discovery -t st -p l1
```
Find the newly created "/default" file:
```
find /etc/iscsi/send_targets/
```

Edit the "...default/default" file, replace:
```
node.session.auth.authmethod = None
```
with:
```
node.session.auth.authmethod = CHAP
node.session.auth.username = bankminus-iscsi-user1
node.session.auth.password = $$PASSWORD1_HERE$$
node.session.auth.username_in = bankminus-iscsi-target2
node.session.auth.password_in = $$PASSWORD2_HERE$$
node.startup = automatic
```

Now connect
```
iscsiadm  -m node  --targetname "iqn.2018-12.bankminus:btrfs-lnd" --portal l1:3260 --login
```

A new sd* device should appear. Find it like this:
```
ls /dev/sd*
```

Check connections (initiator to target) on initiator
```
iscsiadm -m session
```


### BTRFS 

RAID-1

Create filesystems Bitcoin and LND nodes
```
sudo mkfs.btrfs /dev/mmcblk0p3
sudo mkfs.btrfs /dev/mmcblk0p4
```

Mount
```
sudo mkdir /mnt/btrfs_lnd
sudo mount /dev/mmcblk0p4 /mnt/btrfs_lnd
```

Label it
```
sudo btrfs fi label /mnt/btrfs_lnd lnd
sudo btrfs fi label /mnt/btrfs_bitcoind bitcoind

```

Add it to fstab on host `b1`:
```
sudo su -l
echo -e "LABEL=bitcoind\t/mnt/btrfs_bitcoind\tbtrfs\tnoauto\t0\t0" >> /etc/fstab
```

Add it to fstab on host `l1`:
```
sudo su -l
echo -e "LABEL=lnd\t/mnt/btrfs_lnd\tbtrfs\tnoauto\t0\t0" >> /etc/fstab
```


Now you can mount it like this (even if block device names change):
```
sudo mount /mnt/btrfs_lnd
```

Check BTRFS sizes like this (--si makes numbers compatible with numbers in `parted`):
```
sudo btrfs fi show --si
```

If you need to shrink BTRFS you can do so safely, yet you'll need to re-size the device partition table accordingly, e.g.:
```
sudo parted /dev/mmcblk0
```
(type "p" and press enter to see the current partition table)


To setup Raid1 you can do it at the time of running `mkfs.btrfs` or add a new device later, like this:
```
sudo btrfs dev add -f /dev/mmcblk0p4 /mnt/btrfs_lnd

# check current Raid setup
sudo btrfs fi df /mnt/btrfs_lnd

# convert to Raid1
sudo btrfs balance start -dconvert=raid1 -mconvert=raid1 /mnt/btrfs_lnd/
```
For more on BTRFS Raid see https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices#Adding_new_devices 

## Software

### Build Bitcoind

```
sudo adduser bitcoin

mkdir /mnt/btrfs_bitcoind/bin
mkdir /mnt/btrfs_bitcoind/bitcoin
mkdir /mnt/btrfs_bitcoind/src_github.com
chown -R bitocoin /mnt/btrfs_bitcoind/

sudo su -l bitocoin

ln -s /mnt/btrfs_bitcoind/bin
ln -s /mnt/btrfs_bitcoind/bitcoin .bitcoin

echo 'export PATH=$HOME/bin/bin:$PATH  # bitcoind is here' >> ~/.profile
. ~/.profile
```

Follow instruction to build bitoin core: https://github.com/alevchuk/minibank/tree/master/bitcoin


### Start Bitcoind

```
sudo su -l bitocoin
bitcoind
```

### Build Go

Prerequisites:
* Raspbian GNU/Linux 9

Citations:
* This section is based on https://golang.org/doc/install/source and https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#build-go



1. Log-in as user "lightning"


```
sudo adduser lightning

sudo mkdir /mnt/btrfs_lnd/lnd-data
sudo mkdir /mnt/btrfs_lnd/gocode
sudo mkdir /mnt/btrfs_lnd/lnd-e2e-testing
sudo mkdir /mnt/btrfs_lnd/src

sudo chown -R lightning /mnt/btrfs_lnd/

su -l lightning

ln -s /mnt/btrfs_lnd/lnd-data ~/.lnd

ln -s /mnt/btrfs_lnd/gocode
ln -s /mnt/btrfs_lnd/lnd-e2e-testing
ln -s /mnt/btrfs_lnd/src
```

2. Follow instrutions under https://github.com/alevchuk/minibank/blob/master/go/



### Build LND


Follow https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md#installing-lnd


### Start LND

## Monitoring

### Node exporters

Prerequisites:
* Filesystem for LND node
* Build Go

Citations:
 * This section is based on https://github.com/prometheus/prometheus#building-from-source

Install on all nodes.

```
sudo mkdir /mnt/btrfs_lnd/gocode
sudo mkdir /mnt/btrfs_lnd/src
sudo chown -R monitoring /mnt/btrfs_lnd

sudo su -l monitoring
cd ~
ln -s /mnt/btrfs_lnd/src
ln -s /mnt/btrfs_lnd/gocode
```

Now [Build Go](#build-go)

```
go get github.com/prometheus/node_exporter
cd ${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter
make
```

Run exporter
```
./node_exporter 
```


### Prometheus

Install this on the base station to pull in all metrics into a single place.

Setup accounts:
```
sudo adduser prometheus
sudo mkdir /mnt/btrfs/prometheus_gocode
sudo mkdir /mnt/btrfs/prometheus_data

sudo chown prometheus /mnt/btrfs/prometheus_gocode
sudo chown prometheus /mnt/btrfs/prometheus_data

su -l prometheus
ln -s /mnt/btrfs/src ~/lightning_src # symlink to read-only go installation
ln -s /mnt/btrfs/prometheus_gocode/ ~/gocode
```

Fetch source code:
```
go get github.com/prometheus/prometheus/cmd/...
```

Build:
```
cd /home/prometheus/gocode/src/github.com/prometheus/prometheus/
make build
```

Configure:
```
mkdir /mnt/btrfs/prometheus_data
ln -s /mnt/btrfs/prometheus_data ~/.prometheus
vi ~/.prometheus/prometheus.yml
```
Configure to collect from node exporters from all managed hosts, including self, e.g.:
```
scrape_configs:
- job_name: 'node'
  static_configs:
  - targets: ['b1:9100', 'l1:9100', 'base:9100']
```

Run prometheus:
```
prometheus --config.file=$HOME/.prometheus/prometheus.yml --storage.tsdb.path=$HOME/.prometheus/data
```

### Grafana

Grafana is a monitoring/analytics web interface. This is a web server. Install it on the base station.

Citations:
* This section is based on http://docs.grafana.org/project/building_from_source/

Prereqisits:
* [Build Go](#build-go) 
* node exporter running on all nodes
* prometheus of `base`
* ssh into `base`

```
sudo adduser grafana
sudo mkdir /mnt/btrfs/src_grafana
sudo mkdir /mnt/btrfs/gocode_grafana
sudo mkdir /mnt/btrfs/bin_grafana

sudo chown grafana /mnt/btrfs/src_grafana
sudo chown grafana /mnt/btrfs/gocode_grafana
sudo chown grafana /mnt/btrfs/bin_grafana

su -l grafana
ln -s /mnt/btrfs/src ~/src_readonly # symlink to read-only go installation
ln -s /mnt/btrfs/src_grafana ~/src
ln -s /mnt/btrfs/gocode_grafana ~/gocode
ln -s /mnt/btrfs/bin_grafana ~/bin
```

to `~/.profile` add:
```
export GOROOT=~/src_readonly/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH

export PATH=$HOME/bin/bin:$PATH
```


Install grafana:

```
go get github.com/grafana/grafana

cd $GOPATH/src/github.com/grafana/grafana
go run build.go setup
go run build.go build    
```

Build node.js (includes NPM)

```
cd ~/src
git clone https://github.com/nodejs/node.git
git fetch
git checkout v11.2.0
cd node
./configure --prefix $HOME/bin
make
make install
```

Build Grafana front-end:
```
cd $GOPATH/src/github.com/grafana/grafana

npm install -g yarn

# IMPORTANT: before running `yarn install` you need to remove
#            "phantomjs-prebuilt" form ./github.com/grafana/grafana/package.json
#            more details on this here
#            https://github.com/grafana/grafana/issues/14115

yarn install --pure-lockfile
yarn watch
```

Run grafana:
```
cd ~/gocode/src/github.com/grafana/grafana
./bin/linux-arm/grafana-server
```

Update firefall:
```
sudo vi /etc/iptables/rules.v4
```
Add rule (modify -s if your subnet is different):
```
# Allow Grafana Web UI on local network
-A INPUT -p tcp -s 192.168.0.0/24 --dport 3000 -j ACCEPT
```
Reload firewall:
```
sudo systemctl restart netfilter-persistent.service
```


Use grafana: connect your browser to http://localhost:3000

Follow web-ui wizard. Import dashboards node_exporter for Grafana app store.
E.g. "Node Exporter Server Metrics" can show multiple nodes side-by-side:


![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")




## Service Manager

Minibank uses `systemd` to make sure all processes are started in the right order and keep running even after crashes


