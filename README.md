# minibank
bitcoin lightning node

![model 4](https://raw.githubusercontent.com/alevchuk/minibank/master/minibank-2019-08-11.jpg "minibank model 4, Pi 4, 4 GB RAM, 500GB SSD, running mainnet LND")

For older versions see https://github.com/alevchuk/minibank/blob/master/other-notes/HISTORY.md

Table of contents
=================

**WARNING: The work described here is a prototype and not ready for general use...**


  * [Hardware](#hardware)
  * [Network](#network)
  * [Storage](#storage)
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
 
## Hardware

### Model 4 :: Node at Home

* Pi 4: https://camelcamelcamel.com/CanaKit-Raspberry-Basic-Kit-2GB/product/B07TYK4RL8
* Samsung 500 GB SSD (for Raid-1 mirror): https://camelcamelcamel.com/Samsung-T5-Portable-SSD-MU-PA500B/product/B073GZBT36
* SanDisk 500 GB SSD (for Raid-1 mirror): https://camelcamelcamel.com/SanDisk-500GB-Extreme-Portable-External/product/B078SWJ3CF
* Micro HDMI adaptor (for one-time setup): https://camelcamelcamel.com/UGREEN-Adapter-Compatible-Raspberry-ZenBook/product/B00B2HORKE


### (Optional) Model 1 :: Monitoring Station at Home

* Pi 3 B+ https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW
* 2x Micro SD cards https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q
* Touchscreen https://camelcamelcamel.com/Raspberry-Pi-7-Touchscreen-Display/product/B0153R2A9I
* Card Reader https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4
* Case https://camelcamelcamel.com/Case-Official-Raspberry-Touchscreen-Display/product/B01HV97F64

###  (Optional) VM :: Node on Amazon EC2

* 2x Linux on t2.micro
* Storage: 5G general purpose SSD for opearting system
* Storage: 64GB Magnetic Amazon EBS Volumes for software and data

Amazon pricing: http://calculator.s3.amazonaws.com/index.html#r=IAD&s=EC2&key=calc-3E66A912-F5FF-4323-84EF-C7C14F363459



## Operating System

1. Download the image the Raspberry Pi Foundation’s official supported operating system
**Raspbian Buster Lite** from https://www.raspberrypi.org/downloads/raspbian/
3. Uncompress the file: `unzip 2019-07-10-raspbian-buster-lite.zip`
2. Transfer the contents on the ".img" file to your SD card (I use `dd`, Raspberry Pi has instcutions for doing this from [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md), [Mac](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md), and [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md))

> for Amazon EC2 AWS use [Debian GNU/Linux 9 (Stretch)](https://aws.amazon.com/marketplace/pp/B073HW9SP3) 

## First time login

Don't connect to network.

Connect monitor and keyboard. Power-up Pi. Login: `pi` Passowrd: `rpaspberry`


## Network

### Remote Login

Connect via monitor and keyboard.

1. Setup [no-incomming-connections firewall](https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#security) before connecting to the network! If you don't add a firewall you'll get hacked.
Now the output of `sudo iptables-save` should look like this:
```
*filter
:INPUT DROP [152:211958]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [52247:3125304]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
COMMIT
```
2. Changed the password in `rspi-config`. Select: **Change Password** If you don't change the password you'll get hacked.
3. Connect enthernet cable
4. Update the system: `sudo apt-get update; sudo apt-get upgrade;`. If you don't upgrade you'll get hacked.
5. Write down your IP adress. To look it up run `ifconfig`
6. Enable remote login over SSH. Run `rspi-config` select **Interface Options -> SSH -> SSH server to be enabled**
7. Allow SSH in the firewall `sudo vi /etc/iptables/rules.v4` then add "Allow SSH" line so it's like this:
```
*filter
:INPUT DROP [152:211958]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [52247:3125304]
-A INPUT -i lo -j ACCEPT

# Allow SSH !
-A INPUT -p tcp -s 192.168.0.0/16 --dport 22 -j ACCEPT

-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
COMMIT
```
8. Optionally [setup Wi-Fi](https://github.com/alevchuk/minibank/blob/master/other-notes/wifi.md)
9. From your laptop, use the IP from step 5 and run: `ssh pi@YOUR_IP_HERE` enter your new password

### Authorized keys

So you don't have to type the password every time you need to log-in to the pi, setup autorized_key.

On your laptop run:
```
ssh-keygen -f ~/.ssh/minibank_id_rsa
```
Hit enter twice when prompted for password.

Print you're new public key:
```
cat  ~/.ssh/minibank_id_rsa.pub
```

Copy the output to clip-board.

SSH into your Pi and run:
```
cat > ~/.ssh/autorized_keys
```
paste the pubkey from clipboard, press Enter, and then press Ctrl-d.

Now run:
```
chmod o=,g= ~/.ssh/authorized_keys
```
Now log out, press Ctrl-d.

Now try logging back in like this:
```
ssh -i ~/.ssh/minibank_id_rsa pi@YOUR_IP_HERE
```
You should not need to re-enter password.

Finally, back on your laptop, add an alias
```
echo 'alias mb4="ssh -i ~/.ssh/minibank_id_rsa pi@YOUR_IP_HERE"' >> ~/.bash_profile
. ~/.bash_profile
```

Now type `mb4` and that should log you into the Pi.


## Storage

In this section will setup a Raid-1 Mirror from your two new SSD drives.

WARNING: any data in the SSD drives will be deleted.

### Look up block device names

Run `dmesg --follow` and un-plung/re-plug the external SSD drives one by one.

Look for "sd" followed by a small english letter. Write that down.

Also write down which drive it belongs to.

From now I will refer to these as:
* YOUR_SSD_BLOCK_DEVICE_1
* YOUR_SSD_BLOCK_DEVICE_2

The relevant output of `dmesg --follow` would look like this:
![Block Device name lookup](https://raw.githubusercontent.com/alevchuk/minibank/master/block_device_name_lookup.png "Block Device name lookup")


### BTRFS RAID-1 Mirror

Install BTRFS progs:
```
sudo apt-get install btrfs-progs
```

WARNING: any data in the SSD drives will be deleted. If you don't konw what your doing, try running the command without `--force` first.

Create filesystems Bitcoin and LND nodes
```
sudo mkfs.btrfs --force /dev/YOUR_SSD_BLOCK_DEVICE_1_NAME_HERE
sudo mkfs.btrfs --force /dev/YOUR_SSD_BLOCK_DEVICE_2_NAME_HERE
```

Mount
```
sudo mkdir /mnt/btrfs
sudo mount /dev/YOUR_SSD_BLOCK_DEVICE_1_NAME_HERE /mnt/btrfs
```

Label it
```
sudo btrfs fi label /mnt/btrfs minibank4

```

Add it to fstab:
```
sudo su -l
echo -e "LABEL=minibank4\t/mnt/btrfs\tbtrfs\tnoauto\t0\t0" >> /etc/fstab
```

Now you can mount it like this (even if block device names change):
```
sudo mount /mnt/btrfs
```

Check BTRFS sizes like this (--si makes numbers compatible with numbers in `parted`):
```
sudo btrfs fi show --si
```


To setup Raid1 mirror you can do it at the time of running `mkfs.btrfs` or add a new device later, like this:
```
sudo btrfs dev add -f /dev/YOUR_SSD_BLOCK_DEVICE_2_NAME_HERE /mnt/btrfs

# check current Raid setup
sudo btrfs fi df /mnt/btrfs

# convert to Raid1 mirror
sudo btrfs balance start -dconvert=raid1 -mconvert=raid1 /mnt/btrfs/
```

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

Follow instruction to build bitcoin core: https://github.com/alevchuk/minibank/tree/master/bitcoin


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

### Heat

Now it's a good time to [attach Heatsink and start the fan](https://blog.hackster.io/do-you-need-to-use-a-fan-for-cooling-with-the-new-raspberry-pi-4-6d523ca12453). Connect the red cord of the fan to GPIO pin 4 and the black to pin 6.

To measure the temperature, run:
```
while :; do /opt/vc/bin/vcgencmd measure_temp; sleep 1; done
```

### Convenience stuff

While your chain syncs...

#### Host name
Give your host a name. Edit 2 files replacing "raspberrypi" with the name you came up with.
```
sudo vi /etc/hostname
sudo vi /etc/hosts
```
you'll see the change after logging out of SSH (press Ctrl-d) and logging back in.

#### Time-zone

Run `rspi-config` and select **Localization Options --> Change Timezone** to make your system clock right. Check time by running `date`


### Build Go

Prerequisites:
* Raspbian GNU/Linux 9

Citations:
* This section is based on [golang official instructions](https://golang.org/doc/install/source) and [alevchuk/pstm](https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#build-go)


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


![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")



