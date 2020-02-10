# minibank
bitcoin lightning node

![model 4](https://raw.githubusercontent.com/alevchuk/minibank/master/minibank-2019-08-11.jpg "minibank model 4, Pi 4, 4 GB RAM, 500GB SSD, running mainnet LND")

* For older models see [History](https://github.com/alevchuk/minibank/blob/master/other-notes/HISTORY.md)
* For improved reading experience use [https://alevchuk.github.io/minibank/](https://alevchuk.github.io/minibank/)

Table of contents
=================

  * [Hardware](#hardware)
  * [Operating System](#operating-system)
  * [Network](#network)
  * [Storage](#storage)
    * [BTRFS RAID-1 Mirror](#btrfs-raid-1-mirror)
  * [Software](#software)
    * [Build Bitcoin](#build-bitcoind)
    * [Start Bitcoin](#start-bitcoind)
    * [Heat](#heat)
    * [Convenience stuff](#convenience-stuff)
    * [Install Tor](#install-tor)
    * [Install Go](#install-go)
    * [Build LND](#build-lnd)
    * [Start LND](#start-lnd)
      * [Create your Lightning wallet](#create-your-lightning-wallet)
      * [Fund your LND wallet and enable AutoPilot](#fund-your-lnd-wallet-and-enable-autopilot)
      * [Keep track of your total balance](#keep-track-of-your-total-balance)
    * [Open LND port on your router](#open-lnd-port-on-your-router)
    * [Install LND operations scripts](#install-lnd-operations-scripts)
  * [Monitoring](#monitoring)
    * [Prometheus exporters](#prometheus-exporters)
      * [Host Metrics](#host-metrics)
      * [Bitcoin Metrics](#bitcoin-metrics)
    * [Prometheus](#prometheus)
    * [Grafana](#grafana)
  * [Operatons](#operations)
    * Failed SSD drive
    * Temporary connection failure to SSD drive 
 
## Hardware

### Model 4 :: Node at Home

The powerful Pi 4 with plenty of RAM removing the need for swap. Two high-speed SSDs for Raid-1 mirroring. Different manufacturers so they don't fail at the same time.

* Pi 4 kit (4GB RAM, heat sinks, fan, micro-hdmi cable): [CanaKit-Raspberry-4GB-Basic-Starter](https://camelcamelcamel.com/CanaKit-Raspberry-4GB-Basic-Starter/product/B07VYC6S56)
* Micro SD card [Samsung-MicroSDXC-Adapter-MB-ME64GA-AM](https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q)
* Card Reader (for 1 time setup) [Transcend-microSDHC-Reader-TS-RDF5K-Black](https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4)
* Samsung 500 GB SSD (for Raid-1 mirror): [Samsung-T5-Portable-SSD-MU-PA500B](https://camelcamelcamel.com/Samsung-T5-Portable-SSD-MU-PA500B/product/B073GZBT36)
* SanDisk 500 GB SSD (for Raid-1 mirror): [SanDisk-500GB-Extreme-Portable-External](https://camelcamelcamel.com/SanDisk-500GB-Extreme-Portable-External/product/B078SWJ3CF)



### (Optional) Model 1 :: Monitoring Station at Home

* Pi 3 B+ [ELEMENT-Element14-Raspberry-Pi-Motherboard](https://camelcamelcamel.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/product/B07BDR5PDW)
* 2x Micro SD cards [Samsung-MicroSDXC-Adapter-MB-ME64GA-AM](https://camelcamelcamel.com/Samsung-MicroSDXC-Adapter-MB-ME64GA-AM/product/B06XX29S9Q)
* Card Reader [Transcend-microSDHC-Reader-TS-RDF5K-Black](https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4)

###  (Optional) VM :: Node on Amazon EC2

* 2x Linux on t2.micro
* Storage: 5G general purpose SSD for operating system
* Storage: 64GB Magnetic Amazon EBS Volumes for software and data

Amazon pricing: [AWS Calculator File](http://calculator.s3.amazonaws.com/index.html#r=IAD&s=EC2&key=calc-3E66A912-F5FF-4323-84EF-C7C14F363459)



## Operating System

1. Download the image the Raspberry Pi Foundation’s official supported operating system
**Raspbian Buster Lite** from [official raspberrypi link](https://www.raspberrypi.org/downloads/raspbian/)
3. Uncompress the file: `unzip 2019-07-10-raspbian-buster-lite.zip`
2. Transfer the contents on the ".img" file to your SD card (I use `dd`, Raspberry Pi has instcutions for doing this from [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md), [Mac](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md), and [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md))

### (Optional) AWS + Upgrade Debian
Instead of using a Rasberry Pi at your home, you can test in the cloud with Amazon AWS.

Unofortantly AWS does not have an officeian Debian 10 (Buster) image, only 9 (Stretch). So we need to upgrade:
> for Amazon EC2 AWS use [Debian GNU/Linux 9 (Stretch)](https://aws.amazon.com/marketplace/pp/B073HW9SP3) and then upgrade to Debain 10 (Buster)

This upgrade is based on the [cyberciti.biz manual](https://www.cyberciti.biz/faq/update-upgrade-debian-9-to-debian-10-buster/)

1. In AWS console take a snapshot for a backup of the hard drive.

2. Replace /etc/apt/sources.list with new version:
```
sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list
```
3. Refresh apt cache:
```
sudo apt update
```
4. Pre upgrade some packages. When prompted say "yes" to everything, except for **NTP (network time)** say "N" (hit Enter) to keep current config and for **Configuring openssh-server** also hit Enter to keep current config, and for **Grub (boot loader)** continue without installing anything:
```
sudo apt upgrade
```
5. Do the actual upgrade:
```
sudo apt full-upgrade
```
6. Reboot:
```
sudo reboot
```
7. Remove unused packages:
```
sudo apt autoremove
```

## First-time login

Don't connect to network.

Connect monitor and keyboard. Power-up Pi. Login: `pi` Password: `rpaspberry`


## Network

### Remote Login (AWS node)

If your seting up Rasperry Pi node at home then skip this section and proceed to **Remote Login (Home node)**.

AWS has a default firewall setup for you. You can manage it from the Amazon AWS web console under Security Groups. Yet, to be sure your in control, you should also setup a local firewall.

NOTE: In this setup it's easy to make a mistake and get locked out of the remote server, so I recomend takeing a snapshot of the root-drive in AWS at this point in time.


```
sudo apt install iptables-persistent
sudo iptables-save  # show current rules
```

With your favourite command-line text editor, e.g. `sudo vi /etc/iptables/rules.v4` edit /etc/iptables/rules.v4
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
COMMIT
```


Duplicate this initial setup to /etc/iptables/rules.v6
* We allow SSH in IPv6 rules as well in case AWS IPv4 network has issues and we need to be able to log-in. Other than SSH no need to edit any other rules in this file because we are not going to use IPv6 here. 
```
sudo cp /etc/iptables/rules.v4 /etc/iptables/rules.v6
```

Run 
```
sudo /etc/init.d/netfilter-persistent restart
```


### Remote Login (Home node)

Connect via monitor and keyboard.

1. Setup [no-incomming-connections firewall](https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#security) **before connecting to the network!** If you don't add a firewall you'll get hacked:

```
sudo apt install iptables-persistent
sudo iptables-save  # show current rules
```

With your favourite command-line text editor, e.g. `sudo vi /etc/iptables/rules.v4` edit /etc/iptables/rules.v4
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
COMMIT
```

Edit /etc/iptables/rules.v6
```
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
COMMIT
```


Now the output of `sudo iptables-save` should look like this:

 * numbers at the end of the line may be different, those are your network statistics
 
```
*filter
:INPUT DROP [152:211958]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [52247:3125304]
-A INPUT -i lo -j ACCEPT
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
-A OUTPUT -o lo -j ACCEPT

# <-------- Allow SSH from home network only !
-A INPUT -p tcp -s 192.168.0.0/16  --dport 22 -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

COMMIT
``` 
* Leave IPv6 rules as the inital "Drop-everything" setup because most home networks do not need IPv6.
* If this is on Amazon then see **Remote Login (HomeAWS node)** section above.

Run 
```
sudo /etc/init.d/netfilter-persistent restart
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

Copy the output to clipboard.

SSH into your Pi and run:
```
cat >> ~/.ssh/autorized_keys
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


## Storage (AWS node)

If you're setting-up Raspbery Pi at Home then skip this section.

Usually your root drive will not be large enough to host a full Bitcoin node (310G in 2020 + account for future growth) so create a separate EBS (Elastic Block Store) device, format it, and mount it under /mnt/btrfs

```
sudo mkdir /mnt/btrfs

# more steps here to format and mount EBS to /mnt/btrfs
# you can format it as any filesystem (does not have to be BTRFS) yet keep the name or symlic at /mnt/btrfs because we use this in the rest of the manual
```


## Storage (Home node)

If your seting up an Amazon AWS instatnce (not Raspbery Pi at Home) then skip this section.

In this section will setup a Raid-1 Mirror from your two new SSD drives.

WARNING: any data in the SSD drives will be deleted.

### Lookup block device names

Run `sudo dmesg --follow` and un-plung/re-plug the external SSD drives one by one.

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
sudo apt install btrfs-progs
```

WARNING: any data in the SSD drives will be deleted. If you don't know what your doing, try running the command without `--force` first.

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

1. Create bitcoin user unix account
```
sudo adduser --disabled-password bitcoin

sudo mkdir /mnt/btrfs/bitcoin
sudo mkdir /mnt/btrfs/bitcoin/bin
sudo mkdir /mnt/btrfs/bitcoin/dot-bitcoin-data
sudo mkdir /mnt/btrfs/bitcoin/src

sudo chown -R bitcoin /mnt/btrfs/bitcoin

sudo su -l bitcoin

ln -s /mnt/btrfs/bitcoin/bin ~/bin
ln -s /mnt/btrfs/bitcoin/src ~/src
ln -s /mnt/btrfs/bitcoin/dot-bitcoin-data ~/.bitcoin

echo 'export PATH=$HOME/bin/bin:$PATH  # bitcoind is here' >> ~/.profile
. ~/.profile
```

2. Follow instruction to build bitcoin: [alevchuk/minibank/bitcoin](https://github.com/alevchuk/minibank/tree/master/bitcoin)


### Start Bitcoind

Prerequisites:
* Build Bitcoind

Log-in as bitcoin
```
sudo su -l bitcoin
```

Edit `~/.bitcoin/bitcoin.conf`
```
server=1
deamon=0
disablewallet=1

# Bind to given address to listen for JSON-RPC connections. Use [host]:port notation for IPv6.
# This option can be specified multiple times (default: bind to all interfaces)
####rpcbind=<addr>:<port>
####rpcbind=192.168.0.17:8332
rpcbind=127.0.0.1:8332


# By default, only RPC connections from localhost are allowed.
# You can speficy multiple rpcallowip lines to allow different IPs
####rpcallowip=<addr>
####rpcallowip=192.168.0.17
rpcallowip=127.0.0.1

rpcuser=$$PASSWORD_1_HERE$$ 
rpcpassword=$$PASSWORD_2_HERE$$ 

# Listen for RPC connections on this TCP port:
####rpcport=8332

onlynet=ipv4
zmqpubrawblock=tcp://0.0.0.0:29000
zmqpubrawtx=tcp://0.0.0.0:29001

### prune=  # No prune, were running a full node
txindex=1  # Maintain a full transaction index, LND uses this, otherewise there will be a lot of disk scans

dbcache=200  # Maximum database cache size <n> MiB
maxorphantx=10  # Keep at most <n> unconnectable transactions in memory (default: 100)
maxmempool=50  # Keep the transaction memory pool below <n> megabytes
maxconnections=20  # Maintain at most <n> connections to peers
maxuploadtarget=50  # MiB/day for the community

# Detailed logging
####debug=bench
####debug=db
####debug=reindex
####debug=cmpctblock
####debug=coindb
####debug=leveldb
```

You'll need to set things like $$PASSWORD_1_HERE$$ and $$PASSWORD_2_HERE$$ with unique passwords. Generate random strings (of 30 alphanumeric characters) for each password. First character should be a letter. `rpcuser` should also look like a password. Try using: `openssl rand -base64 32 | grep -o '[a-z0-9]' | xargs | tr -d ' '` to generate random strings.

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

While your bitcoin chain syncs...

Skip the following sections if your setting up a node on Amazon AWS or Google cloud:
* Name your Pi
* Time-zone
* Non-British Keyboard

#### Name your Pi

Give your host a name. Edit 2 files replacing "raspberrypi" with the name you came up with. No spaces or punctuation.
```
sudo vi /etc/hostname
sudo vi /etc/hosts  # edit the line with 127.0.1.1
```

you'll see the change after rebooting, run sudo reboot, re-SSH back in run `sudo mount /mnt/btrfs/` and resume the chain sync:
```
sudo su -l bitcoin
bitcoind
```

#### Time-zone


Run `rspi-config` and select **Localization Options --> Change Timezone** to make your system clock right. Check time by running `date`

#### Non-British Keyboard

When attaching with Monitor and a US Keyboard, you may find that your not able to type things like "|". This is not a problem when going over SSH. Yet the fix this replace 
```
XKBMODEL="pc105"
XKBLAYOUT="gb"
```
with
```
XKBMODEL="pc104"
XKBLAYOUT="us"
```
in /etc/default/keyboard


#### bash-completion

```
sudo apt install bash-completion
```


#### Vim

More text editing features.
 
```
sudo apt install vim
```
This will replace "vi" as well.

Vi has a very inconvenient feature of making selection not native to the OS that your SSHing from.

To make selection for Copy-and-paste use laptop's OS instead of staying in Vi, run
```
sudo su -c "echo set mouse= >> /usr/share/vim/vim81/defaults.vim"
```


#### Bash

To the end of `~/.bashrc` add
```
# https://unix.stackexchange.com/a/48113/4058
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it
# Save and reload the history after each command finishes
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
```


#### GNU Screen

```
sudo apt install screen
```

To the end of default screen config add the following lines by running `sudo vi /etc/screenrc` 
```
startup_message off

escape ^Bb
defscrollback 6000
maptimeout 0
defhstatus "^EH"
hardstatus alwayslastline '%{= G}[ %{G} %h %{g} ][%= %{= w}%?%-Lw%?%{= B}%n*%f %t%?%{= B}(%u)%?%{= w}%+Lw%?%= %{= g}][%{B} %Y-%m-%d %{W}%c %{g}]'
```

Note: `%h` puts in the host name. On clould instalations, since you don't control the hostname, instead of `alwayslastline '%{= G}[ %{G} %h %{g} ]` put `alwayslastline '%{= G}[ %{G} YOUR_NODE_NAME_HERE %{g} ]`

Now you can re-start bitcoin in screen, log-out, and it will continue running. To do that:
1. Find where `bticoind` is currently running, click on that, and press Ctrl-c
2. Wait for bitcoin to exit
3. Run `screen`
4. Start Bitcoin
```
sudo su -l bitcoin
bitcoind
```
Now you don't have to worry about loosing SSH connection or logging out.

To deatch from screen press Ctrl-b and then press "d"

To re-attach, run `screen -r`


### Install Tor

Install Tor
```
sudo apt install tor
```

 * Minibank needs tor version **0.3.3.6** or above. Fortunaly Rasiban 10 already has that. On older distos [build tor from source](https://github.com/alevchuk/minibank/tree/master/tor#build-from-source). 
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

### Install Go

Prerequisites:
* Raspbian GNU/Linux 10

Citations:
* This section is based on [golang official instructions](https://golang.org/doc/install/source) and [alevchuk/pstm](https://github.com/alevchuk/pstm/blob/master/lnd-e2e-testing/README.md#build-go)


#### Setup LND environment

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

2. Add lightning to have access to Tor locally:
```
sudo  addgroup lightning debian-tor
```

3. Log-in as "lightning" user and setup symlinks


```
sudo su -l lightning

ln -s /mnt/btrfs/lightning/lnd-data ~/.lnd
ln -s /mnt/btrfs/lightning/gocode
ln -s /mnt/btrfs/lightning/lnd-e2e-testing
ln -s /mnt/btrfs/lightning/src
```

#### Build Go
3. Follow instrutions under [alevchuk/minibank/go](https://github.com/alevchuk/minibank/blob/master/go/)



### Build LND

Preprequisigtes:
* [Build Go](#build-go)

Follow https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md#installing-lnd

Install package that contains `dig` utility:
```
sudo apt install dnsutils
```

### Start LND

Preprequisigtes:
* [Start Bitcoin](#start-bitcoind)
* [Build LND](#build-lnd)
* System package installed: `dnsutils`



Login as lightning:
```
sudo su -l lightning
```

Edit `~/.lnd/lnd.conf`

```
[Application Options]
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
bitcoind.zmqpubrawblock=tcp://localhost:29000
bitcoind.zmqpubrawtx=tcp://localhost:29001
bitcoind.rpchost=b1
bitcoind.rpcuser=$$PASSWORD_1_HERE$$ 
bitcoind.rpcpass=$$PASSWORD_2_HERE$$ 

[neutrino]

[Litecoin]

[Ltcd]

[Litecoind]

[tor]
; The port that Tor's exposed SOCKS5 proxy is listening on. Using Tor allows
; outbound-only connections (listening will be disabled) -- NOTE port must be
; between 1024 and 65535
tor.socks=9050
tor.active=1
tor.v3=1

[autopilot]
autopilot.active=0
autopilot.maxchannels=3
autopilot.allocation=1.0
; default for most nodes is 20000
autopilot.minchansize=20000
autopilot.maxchansize=50000
```

Replace $$PASSWORD_1_HERE$$ and $$PASSWORD_2_HERE$$ with the same passwords that you set in `~bitcoin/.bitcoin/bitcoin.conf`

Enable bash completion for lncli:
```
cp /home/lightning/gocode/src/github.com/lightningnetwork/lnd/contrib/lncli.bash-completion /etc/bash_completion.d/lncli
# on Debian distros install "bash-completion" and uncomment "enable bash completion" in /etc/bash.bashrc
```

Start:
```
lnd --externalip=$(dig +short myip.opendns.com @resolver1.opendns.com):9735
```


### Create your Lightning wallet



Create a wallet

```
lncli create
```

This will create:
1. Your bitcoin private key stored on disk
2. A mnemonic phrase that you can backup to paper and use to restore the bitcoin funds
3. A password that will need to be entered every time LND starts


### Fund your LND wallet and enable AutoPilot

1. Create a one-time-use address and transfer some bitcoin to it

 ```
lncli newaddress np2wkh  # Nested SegWit address
```

2. Send the funds from an external bitcoin wallet.

3. Check that the funds arrived
```
lncli walletbalance  # will show unconfirmed balance within a few seconds. One confirmation will happen roughly every 10 minutes
```
4. Wait for 6 confirmations. About 1 hour.

5. [Optional] Enable autopilot by changing "autopilot.active=0" to "autopilot.active=1" in lnd.conf
6. Restart LND
7. Then check activity in 1 hour:
```
lncli walletbalance
lncli channelbalance
lncli listchannels  | grep active | sort | uniq -c  # number of open channels
lncli listpeers | grep inbound | uniq -c  # to be a relay you'll need to get inbound peers
```

### Keep track of your total balance

Use [treasury_report.py script](scripts/treasury_report.py)
```
# One-time setup:
mkdir ~/lnd-e2e-testing
curl https://raw.githubusercontent.com/alevchuk/minibank/master/scripts/treasury_report.py > ~/scripts/treasury_report.py
chmod +x ~/scripts/treasury_report.py
~/scripts/treasury_report.py >> ~/balance_history.tab

# Track balance
while :; do echo; (cat ~/balance_history.tab; ~/scripts/treasury_report.py ) | column -t; date; sleep 60; done

# Record balance
~/scripts/treasury_report.py | grep -v Time  >> ~/balance_history.tab
```

As channels open and close you may see total balance go down but should it recover eventually. That's because LND overestimates the fees for the channel closing transactions.



### Open LND port on your router

In your minibank, to `/etc/iptables/rules.v4` add:
```
# Allow LND peers
-A INPUT -p tcp --dport 9712 -j ACCEPT
```
and run 
```
sudo /etc/init.d/netfilter-persistent restart
```

In your home router, forward the port 9735 to the host running LND. Here is [a guide](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) on how to do that.

Test with netcat (nc) from a different host
```
seq 100 | nc -v <external_ip_of_LND_host> 9735
```
Alternetively to netcat you can test with [tcpportchecker](https://www.infobyip.com/tcpportchecker.php)

lnc logs will show
```
  2018-01-08 20:41:07.856 [ERR] CMGR: Can't accept connection: unable to accept connection from <IP>:<PORT>: Act One: invalid handshake version: 49, only 0 is valid, msg=....
```

### Install LND operations scripts

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
 * This section is based on [github.com/prometheus](https://github.com/prometheus/prometheus#building-from-source)

Install on all nodes.

```
sudo adduser --disabled-password monitoring

cd /mnt/btrfs 

sudo mkdir ./monitoring
sudo mkdir ./monitoring/gocode
sudo mkdir ./monitoring/src

sudo chown -R monitoring ./monitoring
```

Loging as "monitoring" user
```
sudo su -l monitoring
ln -s /mnt/btrfs/monitoring/src
ln -s /mnt/btrfs/monitoring/gocode
```

to `~/.profile` add:
```
export GOROOT=~/src_readonly/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH

export PATH=$HOME/bin/bin:$PATH
```

and  now install node exporter

#### Host metrics

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

To `/etc/iptables/rules.v4` add:
```
# monitoring / node_exporter
-A INPUT -p tcp -s 192.168.0.0/16 --dport 9100 -j ACCEPT
```
and run 
```
sudo /etc/init.d/netfilter-persistent restart
```

#### Bitcoin metrics

Requierments
 * python3.7 (e.g. comes with Debian / Rasbpbian 10)

Bitcoin Exporter is used to export bitcoin node metrics to Prometheus

Install pip
```
sudo apt install python3-pip
```

Install vitrualenv

Vitrualenv is the only pip package that you will need to install system-wide. Everything else will be installed locally home directories called virtual environments.

```
sudo pip3 install virtualenv

```

Create a new virtual envirment and install dependencies
```
sudo su -l bitcoin

virtualenv --python=python3.7 monitoring-bitcoind && (
  cd ~/monitoring-bitcoind &&
  . bin/activate &&
  pip3 install \
          prometheus_client \
          python-bitcoinlib \
          riprova
)

```

Download Kevin M. Gallagher's amazing bitcoind-monitor.py maintaned and revamped by Jeff Stein: 

```
git clone https://github.com/jvstein/bitcoin-prometheus-exporter.git ~/jvstein/bitcoin-prometheus-exporter
chmod +x ~/jvstein/bitcoin-prometheus-exporter/bitcoind-monitor.py

```

Run bitcoind-monitor.py
```
(. ~/monitoring-bitcoind/bin/activate && 
  REFRESH_SECONDS=30 ~/jvstein/bitcoin-prometheus-exporter/bitcoind-monitor.py)
  
```

Test
```
curl localhost:8334
```

### Prometheus

Requierments
 * Lightning (because we re-use Go build)
 
If you have multiple nodes, install this on the base station to pull in all metrics into a single place.

Setup accounts:
```
sudo adduser --disabled-password prometheus
sudo mkdir /mnt/btrfs/prometheus
sudo mkdir /mnt/btrfs/prometheus/gocode
sudo mkdir /mnt/btrfs/prometheus/data
sudo mkdir /mnt/btrfs/prometheus/src
sudo mkdir /mnt/btrfs/prometheus/bin

sudo chown -R prometheus /mnt/btrfs/prometheus/

sudo su -l prometheus
ln -s /mnt/btrfs/lightning/src ~/lightning_src # symlink to read-only go installation
ln -s /mnt/btrfs/prometheus/src ~/src
ln -s /mnt/btrfs/prometheus/bin ~/bin
ln -s /mnt/btrfs/prometheus/gocode ~/gocode
```

Build node.js (includes NPM)

```
git clone https://github.com/nodejs/node.git ~/src/node
cd ~/src/node
git fetch
git checkout v13.7.0  # version higher then this will not build on the 32-bit rasbian
./configure --prefix $HOME/bin
make
make install

```


Enable Go. To `~/.profile` add:
```
export GOROOT=~/src_readonly/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$HOME/bin/bin:$PATH

```

Install Yarn:
```
npm install -g yarn
```

Fetch source code and build prometheus:
```
go get github.com/prometheus/prometheus/cmd/...
cd /home/prometheus/gocode/src/github.com/prometheus/prometheus/
make build
```

Configure:
```
ln -s /mnt/btrfs/prometheus/data ~/.prometheus
vi ~/.prometheus/prometheus.yml
```
Configure to collect from node exporters from all managed hosts, including self, e.g.:
```
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

scrape_configs:
- job_name: 'node3'
  static_configs:
  - targets: ['bl3:9100', 'bl4:9100', 'bl5:9100', 'bl3:8334', 'bl4:8334', 'bl5:8334']
```

Run prometheus:
```
cd ~prometheus/.prometheus && ~/gocode/src/github.com/prometheus/prometheus/prometheus --storage.tsdb.retention 5y
```

### Grafana

Grafana is a monitoring/analytics web interface.

Warning: This is a web server, so be especially careful with security.

To install and run Grafana follow [alevchuk/minibank/grafana](https://github.com/alevchuk/minibank/blob/master/grafana/README.md)

![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")



# Operations

This section is planned

For now, use [BTRFS Raid wiki](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices#Adding_new_devices)

