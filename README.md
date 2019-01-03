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

### Model 3 :: LND Node at Home

* 2x Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* 2x Micro SD cards https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q
* 2x Case with USB-A Addon Board https://camelcamelcamel.com/MakerFocus-Raspberry-Required-Connector-Protective/product/B07BK2BR6C
* Power Supply https://camelcamelcamel.com/Tranesca-charger-foldable-Samsung-More-Black/product/B01385COIE

### (Optional) Model 1 :: Monitoring Station at Home

* Pi 3 B+ https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW
* 2x Micro SD cards https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q
* Touchscreen https://camelcamelcamel.com/Raspberry-Pi-7-Touchscreen-Display/product/B0153R2A9I
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Case https://camelcamelcamel.com/Case-Official-Raspberry-Touchscreen-Display/product/B01HV97F64

###  (Optional) VM :: LND Node on Amazon EC2

* 2x Linux on t2.micro
* Storage: Amazon EBS Volumes Magnetic 64GB

Amazon pricing: http://calculator.s3.amazonaws.com/index.html#r=IAD&s=EC2&key=calc-2C220F5D-B5C1-4C06-A7B1-D3538AA531B5




## Operating System

Raspbian Stretch Lite https://www.raspberrypi.org/downloads/raspbian/

> for Amazon EC2 AWS use [Debian GNU/Linux 9 (Stretch)](https://aws.amazon.com/marketplace/pp/B073HW9SP3) 

## Network

Prerequisits:
* Setup [firewall](https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#security) before connecting to the network 

(The changes described in this section need to be applied to all hosts)

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

(The changes described in this section need to be applied to all hosts)

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

Prerequisites:
* [Network](#network)

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

### iSCSI relocation

As part of bootstrapping I first setup one of the host as target and another as initiator. I have two partitions on target that I'm exporting and two local partition of the initiator. So four total. I use BTRFS Raid 1 to have two filesystems (btrfs_lnd and btrfs_bitcoind).

So proceed to BTRFS setup from here, and then come back once that's done...

So step one is to mount both filesystems on the same host. Step two is to re-mount one of those filesystems on the other host. So the end goal both hosts are targets and initiators at the same time.

To stop one of the iSCSI for connecting on-startup, edit the "...default/default" file under /etc/iscsi/send_targets/ and comment out (add a `#` in front) the "automatic" line:
```
#node.startup = automatic
```
you can then reboot the host and see that `/dev/sd*` no longer shows up. Also, the TCP connection will stop showing up when you run:
```
sudo iscsiadm -m session
```

Once one of the connections is removed, go through the "iSCSI" section again to setup target and initiator in the reverse direction.

So the end goal is looks like this:

```
+------------------------------------+              +-------------------------------------------+
|                                    |              |                                           |
|  b1                                |              |  l1                                       |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
|      +-----+   /dev/mmcblk0p3 +-----------X--------------->   /dev/sda                        |
|      |                             |              |                                           |
|      |                             |              |                                           |
|      |         /dev/mmcblk0p4 +-------------------------->    /dev/sdb  +-----------+         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      +-------+  /dev/sda      <--------------------+   /dev/mmcblk0p3               |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |          /dev/sdb     <-------------X--------+  /dev/mmcblk0p4 +-------------+         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      v                             |              |                                 v         |
|                                    |              |                                           |
|      /etc/fstab                    |              |                     /etc/fstab            |
|        LABEL=bitcoind              |              |                       LABEL=lnd           |
|        /mnt/btrfs_bitcoind         |              |                       /mnt/btrfs_lnd      |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
|                                    |              |                                           |
+------------------------------------+              +-------------------------------------------+
```

(Note: /dev/sda /dev/sdb naming is can change, so it's important to use BTRFS labels in fstab instead of specific device names)


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

mkdir /mnt/btrfs_bitcoind/bitcoin
mkdir /mnt/btrfs_bitcoind/bitcoin/bin
mkdir /mnt/btrfs_bitcoind/bitcoin/bitcoin-data
mkdir /mnt/btrfs_bitcoind/bitcoin/src
chown -R bitocoin /mnt/btrfs_bitcoind/bitcoin

sudo su -l bitocoin

ln -s /mnt/btrfs_bitcoind/bitcoin/bin
ln -s /mnt/btrfs_bitcoind/bitcoin/bitcoin-data .bitcoin

echo 'export PATH=$HOME/bin/bin:$PATH  # bitcoind is here' >> ~/.profile
. ~/.profile
```

Follow instruction to build bitoin core: https://github.com/alevchuk/minibank/tree/master/bitcoin


### Start Bitcoind

Prerequisites:
* Build Bitcoind

Log-in as bitcoin
```
sudo su -l bitocoin
```

Edit ~/.bitcoin/bitcoin.conf
```
server=1
deamon=0
disablewallet=1

rpcbind=0.0.0.0
rpcallowip=192.168.0.17
rpcuser=ldjkfhg74y587ye8g985
rpcpassword=akjnf4hwuh49hwei4
#rpcport=18334
onlynet=ipv4
zmqpubrawblock=tcp://0.0.0.0:29000
zmqpubrawtx=tcp://0.0.0.0:29001

#txindex=1
txindex=0
prune=5000

##dbcache=100
dbcache=200  ## trying to impove catch up time, 2018-12-11
maxorphatx=10
maxmempool=50
maxconnections=40
maxuploadtarget=5000
```

Start
```
bitcoind
```

### Build Go

Prerequisites:
* Raspbian GNU/Linux 9

Citations:
* This section is based on https://golang.org/doc/install/source and https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#build-go


#### Setup LND environment

1. Add new user "lightning" and setup storge directories on BTRFS


```
sudo adduser lightning

sudo mkdir /mnt/btrfs_lnd/lightning
sudo mkdir /mnt/btrfs_lnd/lightning/lnd-data
sudo mkdir /mnt/btrfs_lnd/lightning/gocode
sudo mkdir /mnt/btrfs_lnd/lightning/lnd-e2e-testing
sudo mkdir /mnt/btrfs_lnd/lightning/src

sudo chown -R lightning /mnt/btrfs_lnd/lightning
```

2. Log-in as "lightning" user and setup symlinks
```
sudo su -l lightning

ln -s /mnt/btrfs_lnd/lightning/lnd-data ~/.lnd
ln -s /mnt/btrfs_lnd/lightning/gocode
ln -s /mnt/btrfs_lnd/lightning/lnd-e2e-testing
ln -s /mnt/btrfs_lnd/lightning/src
```

#### Build Go
3. Follow instrutions under https://github.com/alevchuk/minibank/blob/master/go/



### Build LND

Preprequisigtes:
* [Build Go](#build-go)

Follow https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md#installing-lnd

Install package that contains `dig` utility:
```
sudo apt-get install dnsutils
```

### Start LND

Preprequisigtes:
* [Start Bitcoin](#start-bitcoind)
* [Build LND](#build-lnd)
* System package installed: `dnsutils`



Login as lightning:
```
su -l lightning
```

Edit ~/.lnd/lnd.conf

```
[Application Options]
nochanupdates=1  ; saves on resources, neccessary to run on Ras Pi Zero
listen=0.0.0.0:9736
rpclisten=localhost:10009
debuglevel=ATPL=debug,CRTR=warn

[Bitcoin]
bitcoin.active=1
bitcoin.testnet=0
bitcoin.mainnet=1
bitcoin.simnet=0
bitcoin.node=bitcoind

[Btcd]

[Bitcoind]
bitcoind.zmqpubrawblock=tcp://b1:29000
bitcoind.zmqpubrawtx=tcp://b1:29001
bitcoind.rpchost=b1
bitcoind.rpcuser=ldjkfhg74y587ye8g985
bitcoind.rpcpass=akjnf4hwuh49hwei4
[neutrino]

[Litecoin]

[Ltcd]

[Litecoind]

[autopilot]
autopilot.active=1
autopilot.maxchannels=3
autopilot.allocation=1.0
autopilot.minchansize=20000  ; default for most nodes is 20000
autopilot.maxchansize=50000

[tor]
```

Start:
```
lnd --externalip=$(dig +short myip.opendns.com @resolver1.opendns.com):9736
```


## Monitoring

### Node exporters

Prerequisites:
* [Storage](#storage)
* [Build Go](#build-go)

Citations:
 * This section is based on https://github.com/prometheus/prometheus#building-from-source

Install on all nodes.

```
sudo mkdir /mnt/btrfs_lnd/monitoring
sudo mkdir /mnt/btrfs_lnd/monitoring/gocode
sudo mkdir /mnt/btrfs_lnd/monitoring/src

sudo chown -R monitoring /mnt/btrfs_lnd/monitoring
```

Now [Build Go](#build-go) or copy it from lightning user like this:
```
sudo mkdir -p /mnt/btrfs_lnd/monitoring/src/go/bin
sudo rsync -a --delete /mnt/btrfs_lnd/lightning/src/go/bin/ /mnt/btrfs_lnd/monitoring/src/go/bin/
sudo rsync -a --delete /mnt/btrfs_lnd/lightning/gocode/ /mnt/btrfs_lnd/monitoring/gocode/
sudo chown -R monitoring /mnt/btrfs_lnd/monitoring
```

Loging as "monitoring" user
```
sudo su -l monitoring
ln -s /mnt/btrfs_lnd/monitoring/src
ln -s /mnt/btrfs_lnd/monitoring/gocode
```

Build None Exporter
```
GO111MODULE=on go get github.com/prometheus/node_exporter
# if you get "net/http: TLS handshake timeout" errors, you need to re-run the `go get` command above 
# if the error is persistent try to see how to make the netwrok less busy (e.g. temporary stop bitcoind)

cd ${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter

GO111MODULE=on make
```

Run node_exporter
```
${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter/node_exporter 
```


### Prometheus

Install this on the base station to pull in all metrics into a single place.

Setup accounts:
```
sudo adduser prometheus
sudo mkdir /mnt/btrfs/prometheus
sudo mkdir /mnt/btrfs/prometheus/gocode
sudo mkdir /mnt/btrfs/prometheus/data

sudo chown -R prometheus /mnt/btrfs/prometheus/

su -l prometheus
ln -s /mnt/btrfs/src ~/lightning_src # symlink to read-only go installation
ln -s /mnt/btrfs/prometheus/gocode ~/gocode
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


