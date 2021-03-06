# minibank Model 3
bitcoin lightning node

![alt text](https://raw.githubusercontent.com/alevchuk/minibank/first/img/minibank-2019-04-07.jpg "minibank model 3, 256GB microSD cards, running mainnet LND")

For older versions see https://github.com/alevchuk/minibank/blob/first/other-notes/HISTORY.md

Table of contents
=================

**WARNING: The work described here is a prototype and not ready for general use...**


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
    * [Open LND port on your router](#open-lnd-port-on-your-router)
    * [Install LND testing scripts](#install-lnd-testing-scripts)
  * [Monitoring](#monitoring)
    * [Prometheus exporters](#prometheus-exporters)
    * [Prometheus](#prometheus)
    * [Grafana](#grafana)
  * [Service Manager](#service-manager)
 
## Hardware

### Model 3 :: Node at Home

* 2x Pi Zero W https://camelcamelcamel.com/Raspberry-Pi-Zero-Wireless-model/product/B06XFZC3BX
* 2x 400GB A1 Micro SD cards https://camelcamelcamel.com/SanDisk-Ultra-microSDXC-Adapter-SDSQUAR-400G-GN6MA/product/B074RNRM2B
* 2x Case with USB-A Addon Board https://camelcamelcamel.com/MakerFocus-Raspberry-Required-Connector-Protective/product/B07BK2BR6C
* Power Supply https://camelcamelcamel.com/Tranesca-charger-foldable-Samsung-More-Black/product/B01385COIE



## Naming hosts

You'll need two Raspberry Pi Zero W (Model 3) one for LND and the other one for Bitcoind. I'll call all of the Pis "hosts" and use the hostnames `l1`, `b1`, and `base` in this manual. 

`base` host is optinal. It's touchscreen Base Station (Model 1) for monitoring. Monitoring consists of a time-series database and a web user interface. 

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

```
sudo apt-get install dphys-swapfile
```

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

I have been running Bitcoind + LND on this setup for over 6 months on two Pi Zero W boards and still have not seen failures related to swap wearing out the microSD cards. For context on why this is important and why it works, see "System with too little RAM" section in [https://askubuntu.com/a/652355/5191].

## Storage

### Partition

The two hosts `b1` and `l1` will have identical SD card partition table. 

```
sudo parted /dev/mmcblk0
```

* First partition is for boot
* Second partition is for operating system
* Third partition is for Lightning Network software and data
* Fourth partition is for Bitcoin software and data

Allocate 50 MB to **First** and 4.5G to **Second** (you probably already have those with the Rasbian image).
Allocate 10G to **Third**, and 241G to **Fourth**.

Use `mkpart` action in `parted`.

To add new partitions type `mkpart` followed by Enter, you be in interative mode where you can type the first letter and press tab to complete the command. If you mess up, you can remove the newly added partitions with `rm`.

WARNING: Only do `rm` freely on new SD cards. Otherwise you're risking to loose data that was there before. To check run `sudo parted /dev/mmcblk0 print` and verify the current set of partitions before performing `rm` actions. 

Adding two partitions should look like this:
```
(parted) mkpart
Partition type?  primary/extended? primary
File system type?  [ext2]? btrfs
Start? 4500MB
End? 14501MB

(parted) mkpart
Partition type?  primary/extended? primary
File system type?  [ext2]? btrfs
Start? 14501MB
End? 256GB

(parted) p
Model: SD GE8QT (sd/mmc)
Disk /dev/mmcblk0: 256GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      4194kB  49.5MB  45.3MB  primary  fat32        lba
 2      50.3MB  4500MB  4450MB  primary  ext4
 3      4500MB  14.5GB  10.0GB  primary  btrfs        lba
 4      14.5GB  256GB   242GB   primary  btrfs        lba    
```

The default in parted is showing sizes the older units of MB=1000^2 of hard-drive manufacturers. Filesystems work in the newer unit of MiB=1024^2 so make sure to double check the final disk size by swithing the units like this:
```
(parted) unit GiB
(parted) p

Number  Start    End      Size     Type     File system  Flags
 1      0.00GiB  0.05GiB  0.04GiB  primary  fat32        lba
 2      0.05GiB  4.19GiB  4.14GiB  primary  ext4
 3      4.19GiB  13.5GiB  9.31GiB  primary  btrfs
 4      13.5GiB  238GiB   225GiB   primary  btrfs
```


> for EC2m, Azure, or Google Cloud attach a 300GiB HDD drive.

### Amazon EC2
> for Amazon EC2 AWS use /dev/xvdb and skip First and Second partitions because that's already on a separate device (/dev/xvda1). So, on EC2 AWS the following should do the trick:
> ```
> sudo parted /dev/xvdb  mklabel msdos
> sudo parted  -a optimal   /dev/xvdb mkpart primary btrfs 0% 10GiB
> sudo parted  -a optimal   /dev/xvdb mkpart primary btrfs 10GB 299.9GiB
> ```
> Amazon EC2 AWS WARNING: `/dev/xvdb` may unexpectedly refer to a drive with valuable data. Only do this on a newly created EC2 instance and mounting a newly created EBS Volume, otherwise you're risking to loose data that was only your previous volumes. To check run `sudo parted /dev/xvdb print` and verify that there were no Partition Table before performing the `mklabel` and `mkpart` actions. 

#### Microsoft Azure (don't bother)
> for Azure use /dev/sdc skip First and Second partitions because that's already on a separate device. So, on Azure the following should do the trick:
> ```
> sudo parted /dev/sdc  mklabel msdos
> ```
> Warning: The existing disk label on /dev/sdc will be destroyed and all data on this disk will be lost. Do you want to >continue? Yes/No? yes
> ```
> sudo parted  -a optimal   /dev/sdc mkpart primary btrfs 0% 10GiB
> sudo parted  -a optimal   /dev/sdc mkpart primary btrfs 10GB 299.9GiB
> ```
> Azure WARNING: `/dev/sdc` may unexpectedly refer to a drive with valuable data. Only do this on a newly created Virtual Machines and mounting a newly created Data Disk, otherwise you're risking to loose data that was only your previous volumes. To check, first run `sudo parted /dev/sdc print` and verify that there were no Partition Table before performing the `mklabel` and `mkpart` actions. 

#### Google Cloud
> for Google Cloud use /dev/sdb , skip First and Second partitions because that's already on a separate device.
> ```
> sudo parted /dev/sdb  mklabel msdos
> ```
> Warning: The existing disk label on /dev/sdb will be destroyed and all data on this disk will be lost. Do you want to >continue? Yes/No? yes
> ```
> sudo parted  -a optimal   /dev/sdb mkpart primary btrfs 0% 10GiB
> sudo parted  -a optimal   /dev/sdb mkpart primary btrfs 10GB 299.9GiB
> ```


### iSCSI

Prerequisites:
* [Network](#network)

(Not needed for Base Station because Base Station will use an external USB Card reader)

iSCSI makes a storage device available over the network. This is useful to avoid cables, USB, and extra card readers.

Notes are based on https://www.tecmint.com/setup-iscsi-target-and-initiator-on-debian-9/ - yet here we avoid using LVM

You'll need to set things like $$PASSWORD1_HERE$$ with unique passwords. Generate random strings (of 30 alphanumeric characters) for each password. 

Part 1: Target (host l1)

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
     incominguser bankminus-iscsi-user1 $$PASSWORD_1_A_HERE$$
     outgoinguser bankminus-iscsi-target1  $$PASSWORD_1_B_HERE$$
</target>
<target iqn.2018-09.bankminus:btrfs-lnd>
     backing-store /dev/mmcblk0p4
     initiator-address 192.168.0.15
     incominguser bankminus-iscsi-user2 $$PASSWORD_2_A_HERE$$
     outgoinguser bankminus-iscsi-target2  $$PASSWORD_2_B_HERE$$
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

Part 2: Initiator (host b1)

On host b1 mount the remote filesystem


```
apt-get install open-iscsi
```

Restart 
``
service open-iscsi restart
``

Discover targets (run this on host b1 - the initiator, host l1 is the target):
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
node.session.auth.password = $$PASSWORD_1_A_HERE$$
node.session.auth.username_in = bankminus-iscsi-target1
node.session.auth.password_in = $$PASSWORD_1_B_HERE$$
node.startup = manual
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
|      +-----+   /dev/mmcblk0p3      |              |                                           |
|      |                             |    iSCSI     |                                           |
|      |         /dev/mmcblk0p4 +-------------------------->    /dev/sda  +-----------+         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |              |                                 |         |
|      |                             |    iSCSI     |                                 |         |
|      +-------+  /dev/sda      <----------------------+ /dev/mmcblk0p3               |         |
|      |                             |              |                                 |         |
|      |                             |              |    /dev/mmcblk0p4 +-------------+         |
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

Prerequisites: 
 * Follow instructions to upgrade kernel and build new BTRFS utility programs https://github.com/alevchuk/minibank/tree/first/btrfs

RAID-1

Create filesystems Bitcoin and LND nodes
```
sudo mkfs.btrfs /dev/mmcblk0p3
sudo mkfs.btrfs /dev/mmcblk0p4
```

Mount
```
sudo mkdir /mnt/btrfs_bitcoind
sudo mount /dev/mmcblk0p3 /mnt/btrfs_bitcoind

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
> don't use compression on the LND filesystem
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

sudo mkdir /mnt/btrfs_bitcoind/bitcoin
sudo mkdir /mnt/btrfs_bitcoind/bitcoin/bin
sudo mkdir /mnt/btrfs_bitcoind/bitcoin/bitcoin-data
sudo mkdir /mnt/btrfs_bitcoind/bitcoin/src

sudo chown -R bitcoin /mnt/btrfs_bitcoind/bitcoin

sudo su -l bitcoin

ln -s /mnt/btrfs_bitcoind/bitcoin/bin ~/bin
ln -s /mnt/btrfs_bitcoind/bitcoin/src ~/src
ln -s /mnt/btrfs_bitcoind/bitcoin/bitcoin-data ~/.bitcoin

echo 'export PATH=$HOME/bin/bin:$PATH  # bitcoind is here' >> ~/.profile
. ~/.profile
```

Follow instruction to build bitcoin core: https://github.com/alevchuk/minibank/tree/first/bitcoin


### Start Bitcoind

Prerequisites:
* Build Bitcoind

Log-in as bitcoin
```
sudo su -l bitcoin
```

Edit ~/.bitcoin/bitcoin.conf
```
server=1
deamon=0
disablewallet=1

# Bind to given address to listen for JSON-RPC connections. Use [host]:port notation for IPv6.
# This option can be specified multiple times (default: bind to all interfaces)
####rpcbind=<addr>

# By default, only RPC connections from localhost are allowed.
####rpcallowip=192.168.0.17

rpcuser=$$PASSWORD_1_A_HERE$$ 
rpcpassword=$$PASSWORD_1_B_HERE$$ 

# Listen for RPC connections on this TCP port:
####rpcport=8332

onlynet=ipv4
zmqpubrawblock=tcp://0.0.0.0:29000
zmqpubrawtx=tcp://0.0.0.0:29001

txindex=1
####prune=  # No prune, were running a full node
####dbcache=200  ## trying to impove catch up time, 2018-12-11
####maxorphatx=10
####maxmempool=50
####maxconnections=20
####maxuploadtarget=50  # MiB/day for the community

# Detailed logging
####debug=bench
####debug=db
####debug=reindex
####debug=cmpctblock
####debug=coindb
####debug=leveldb
```

You'll need to set things like $$PASSWORD_1_A_HERE$$ with unique passwords. Generate random strings (of 30 alphanumeric characters) for each password. First character should be a letter. `rpcuser` should also look like a password. Try using: `openssl rand -base64 32 | grep -o '[a-z0-9]' | xargs | tr -d ' '` to generate random strings.

Start
```
bitcoind
```

### Build Go

Prerequisites:
* Raspbian GNU/Linux 9

Citations:
* This section is based on [golang official instructions](https://golang.org/doc/install/source) and [alevchuk/pstm](https://github.com/alevchuk/pstm/blob/first/lnd-e2e-testing/README.md#build-go)


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
3. Follow instrutions under https://github.com/alevchuk/minibank/blob/first/go/



### Build LND

Preprequisigtes:
* [Build Go](#build-go)

Follow https://github.com/lightningnetwork/lnd/blob/first/docs/INSTALL.md#installing-lnd

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
;; nochanupdates was replaced by numgraphsyncpeers
;; https://github.com/lightningnetwork/lnd/commit/80b84eef9cc7b33b112dcde597fe68ca136a9f40
;; nochanupdates=1  ; saves on resources, neccessary to run on Ras Pi Zero
listen=0.0.0.0:9735
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
bitcoind.rpcuser=$$PASSWORD_1_A_HERE$$ 
bitcoind.rpcpass=$$PASSWORD_1_B_HERE$$ 

[neutrino]

[Litecoin]

[Ltcd]

[Litecoind]

[autopilot]
autopilot.active=1
autopilot.maxchannels=3
autopilot.allocation=1.0

; default for most nodes is 20000
autopilot.minchansize=20000

autopilot.maxchansize=50000

[tor]
```

Enable bash completion for lncli:
```
cp /home/lightning/gocode/src/github.com/lightningnetwork/lnd/contrib/lncli.bash-completion /etc/bash_completion.d/lncli
# on Debian distros install "bash-completion" and uncomment "enable bash completion" in /etc/bash.bashrc
```

Start:
```
lnd --externalip=$(dig +short myip.opendns.com @resolver1.opendns.com):9735
```

### Open LND port on your router

In your home router, forward the port 9735 to the host running LND.

Test with netcat (nc) from a different host
```
seq 100 | nc -v <external_ip_of_LND_host> 9735
```
Alternetively to netcat you can use https://www.infobyip.com/tcpportchecker.php

lnc logs will show
```
  2018-01-08 20:41:07.856 [ERR] CMGR: Can't accept connection: unable to accept connection from <IP>:<PORT>: Act One: invalid handshake version: 49, only 0 is valid, msg=....
```

### Install LND testing scripts

Change into Lighting account:
```
sudo su -l lightning
```

Checkout scripts and copy to `lnd-e2e-testing`:
```
cd ~
git clone https://github.com/alevchuk/minibank.git
rsync -ai ~/minibank/scripts/ ~/lnd-e2e-testing/
```

* close_channel_custom.py
* pay_or_get_paid.py
* rebalance_channels.py
* treasury_report.py

Most of those scripts are short/readable and have internal documentation.

#### Record balance every hour automatically
```
crontab -e
'''

### Text-editor will open, paste the following, save, and exit:

SHELL=/bin/bash
# m h  dom mon dow   command
0   *  *   *   *     (source ~/.profile; ~/lnd-e2e-testing/treasury_report.py --no-header >> ~/balance_history.tab) 2> /tmp/stderr_cron_treasury_report

'''
```

Now you can track the historical + realtime balance like this:
```
# Track balance
while :; do echo; (cat ~/balance_history.tab; ~/lnd-e2e-testing/treasury_report.py ) | column -t; sleep 60; done
```

#### Monitor channels
```
while :; do echo; date; ~/lnd-e2e-testing/rebalance_channels.py; sleep 1m; done
```

Example, output:
```
Mon 25 Mar 21:14:04 UTC 2019
Incative channels:
           chan_id      pubkey       local          remote      remote-pct      mini-id
--------------------------------------------------------------------------------

Active channels:
           chan_id      pubkey       local          remote      remote-pct      mini-id
--------------------------------------------------------------------------------
625373626745421824      0360f95      15789               3          33.33%      1
625357134040268800      02d58ee      15513               6          66.67%      0

Suggested new remote balance percentage --dst-pct 50.00
```

## Monitoring

### Prometheus exporters

Prerequisites:
* [Storage](#storage)
* [Build Go](#build-go)

Citations:
 * This section is based on https://github.com/prometheus/prometheus#building-from-source

Install on all nodes.

```
sudo adduser monitoring

cd /mnt/btrfs_lnd  # or /mnt/btrfs_bitcoind depending on mount on this host

sudo mkdir ./monitoring
sudo mkdir ./monitoring/gocode
sudo mkdir ./monitoring/src

sudo chown -R monitoring ./monitoring
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

#### Node Exporter

Node Exporter is used to export system metrics to Prometheus

```
go get github.com/prometheus/node_exporter
# if you get "net/http: TLS handshake timeout" errors, you need to re-run the `go get` command above 
# if the error is persistent try to see how to make the netwrok less busy (e.g. temporary stop bitcoind)

cd ${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter

git pull

make
```

Run node_exporter
```
${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter/node_exporter 
```

#### Bitcoin Exporter

Bitcoin Exporter is used to export bitcoin node metrics to Prometheus

Install pip
```
sudo apt-get install python3-pip
```

Install vitrualenv

Vitrualenv is the only pip package that you will need to install system-wide. Everything else will be installed locally home directories called virtual environments.

```
sudo pip3 install virtualenv
```

Create a new virtual envirment and install prometheus python client library 
```
sudo su -l bitcoin
virtualenv monitoring-bitcoind -p python3.5
cd ~/monitoring-bitcoind
. bin/activate
pip install prometheus_client
```

Download Kevin M. Gallagher's amazing bitcoind-monitor.py 
https://gist.github.com/ageis/a0623ae6ec9cfc72e5cb6bde5754ab1f

```
curl https://gist.githubusercontent.com/ageis/a0623ae6ec9cfc72e5cb6bde5754ab1f/raw/4aeee711a041c5a25fac4397faee8b8098a4e5d1/bitcoind-monitor.py >  exporter-bitcoind-monitor.py
chmod +x exporter-bitcoind-monitor.py
```

Change shebang to use python3
```
sed -i 's|/usr/bin/python|/usr/bin/python3|g' exporter-bitcoind-monitor.py
```

Run bitcoind-monitor.py
```
. ~/monitoring-bitcoind/bin/activate
~/monitoring-bitcoind/exporter-bitcoind-monitor.py
```

Test
```
curl localhost:8334
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


![alt text](https://raw.githubusercontent.com/alevchuk/minibank/first/img/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")


