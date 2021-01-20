# minibank
bitcoin lightning node

![model 4](https://raw.githubusercontent.com/alevchuk/minibank/first/img/minibank-2020-04-10.jpg "minibank model 4, Pi 4, 4 GB RAM, 500GB SSD, running mainnet LND")

For older models see [History](https://github.com/alevchuk/minibank/blob/first/other-notes/HISTORY.md). For improved reading experience use [https://alevchuk.github.io/minibank/](https://alevchuk.github.io/minibank/)

Table of contents
=================

  * [About](#about)
  * [Hardware](#hardware)
  * [Operating System](#operating-system)
  * [Heat](#heat)
  * [Network](#network)
  * [Storage](#storage-home-node)
    * [Lookup Storage Device Info](#lookup-storage-device-info)
    * [Disable UAS](#disable-uas)
    * [BTRFS RAID-1 Mirror](#btrfs-raid-1-mirror)
  * [Software](#software)
    * [Build Bitcoin](#build-bitcoind)
    * [Start Bitcoin](#start-bitcoind)
    * [Convenience stuff](#convenience-stuff)
    * [Setup LND environment](#setup-lnd-environment)
    * [Install Tor](#install-tor)
    * [Build Go](#build-go)
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
      * [LND Metrics](#lnd-metrics)
    * [Prometheus](#prometheus)
    * [Grafana](#grafana)
  * [Operatons](#operations)
    * Failed SSD drive
    * Temporary connection failure to SSD drive 
 
## About

Minibank is a HOWTO for building a Lightning Network node from scratch
* Limited set of features: bitcoind, lnd, tor 
* Components are built from source code
* Mirror Raid with 2 external storage devices
* Development environment (CLI only) 
* Monitoring

Comparison to similar projects, it the order of difficulty of use:
1. Minibank - for those who like to cook **from scratch**, aims to increase security by limiting surface area / **no add-ons** and building everything from source (paranoid mode) - [CLI Setup] 
2. RaspiBlitz - for technically interested / "geeky" users, building projects, trying stuff out, **tinkering** - [CLI Setup]
3. RoninDojo - **no lightning**, for privacy focused users, maximally focused on Samourai Wallet's Dojo - [CLI Setup]
4. nodl - for less technical users that still want improved security, e.g. merchants - [CLI Setup]
5. nodl Dojo - for privacy focused users, Lightning lnd is available as a 1-click install - [GUI Setup]
6. myNode - for non-technical users, works out of the box, **web interface prioritized** - [GUI Setup]
7. Embassy - for grandma to run Lighting and other self-hosted apps. An operating system by start9labs, they ship a device that you plug into home router and **use a phone app to install self-hosted apps** - [GUI Setup]
8. Umbrel - OS and friendly UI with similar goals as Embassy 

## Hardware

### Model 4 :: Node at Home

The powerful Pi 4 with plenty of RAM removing the need for swap. Two high-speed SSDs for Raid-1 mirroring. Different manufacturers so they don't fail at the same time.

Total **296 USD** as of 2020-12-09

* Pi 4 kit (8GB RAM, heat sinks, power supply): [CanaKit Raspberry Pi 4 Basic Kit 8GB RAM](https://camelcamelcamel.com/product/B08DJ9MLHV)
* FLIRC Passive cooling case [Flirc Raspberry Pi 4 Case](https://camelcamelcamel.com/Flirc-Raspberry-Pi-Case-Silver/product/B07WG4DW52)
* Micro SD card 32G (for operating system) [SanDisk-Extreme-microSD-UHS-I-Adapter](https://camelcamelcamel.com/product/B06XWMQ81P)
* SanDisk 500 GB SSD (for data; Raid-1 mirror): [SanDisk-500GB-Extreme-Portable](https://camelcamelcamel.com/product/B078SWJ3CF)
* SAMSUNG 500 GB SSD (for datat; Raid-1 mirror): [SAMSUNG-500GB-T7-Portable](https://camelcamelcamel.com/product/B0874XJL6M)
* Card Reader (for 1 time setup) [Transcend-microSDHC-Reader-TS-RDF5K-Black](https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4)

Known issues:
* WARNING: DO NOT USE Seagate SSDs. The following Seagate divice caused data corruption when pluging into USB, other storage connected to UBS also got affected. DO NOT USE Seagate 500 GB SSD (for Raid-1 mirror): [Seagate-Barracuda-500GB-External-Portable](https://camelcamelcamel.com/product/B083FF3PJ9)


### (Optional) Monitoring Station at Home

* Same hardware as Node at Home

You can have a dedicated setup for better secutiry or combine LND / BTC / Monitroing into one Pi.


###  (Optional) VM :: Node on Amazon EC2

* 2x Linux on t2.small (2GB RAM is a minimum requirement)
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

2. Get latest update for Stretch:
```
sudo apt update
sudo apt upgrade
```

3. Replace /etc/apt/sources.list with new version:
```
sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list
```

4. Refresh apt cache:
```
sudo apt update
```
5. Pre upgrade some packages. When prompted:
  * when text readers open, press "q" to continue
  * say "yes" to everything, except for **NTP (network time)** say "N" (hit Enter) to keep current config 
  * for **Configuring openssh-server** also hit Enter to keep current config
  * for **Grub (boot loader)** continue without installing anything:
```
sudo apt upgrade
```

6. Do the actual upgrade:
```
sudo apt full-upgrade
```

7. Reboot:
```
sudo reboot
```

8. Remove unused packages:
```
sudo apt autoremove
```

## First-time login

Don't connect to network.

Connect monitor and keyboard. Power-up Pi. Login: `pi` Password: `rpaspberry`



## Heat

I recomend using FLIRC passive cooling:
- Pi temp under 50C
- No more worries of airflow obstruction
- Fan won't fail cuz it ain't got one

If you still want to go with a fan, follow [this howto](https://blog.hackster.io/do-you-need-to-use-a-fan-for-cooling-with-the-new-raspberry-pi-4-6d523ca12453). Tip: Connect the fan to GPIO pins with quiet cooling mode works best for me https://www.raspberrypi.org/forums/viewtopic.php?t=248918#p1519636

To measure the temperature, run:
```
while :; do /opt/vc/bin/vcgencmd measure_temp; sleep 1; done
```

Anything bellow 70C is good. The trotteling [kicks in at 80 C](https://www.theregister.co.uk/2019/07/22/raspberry_pi_4_too_hot_to_handle/).
 

## Network

### Remote Login (home node)

Connect via monitor and keyboard.

1. Setup no-incomming-connections firewall **before connecting to the network!** If you don't add a firewall you'll get hacked:

Run:
```
sudo mkdir /etc/iptables
```

2. Edit /etc/iptables/rules.v4 ith your favourite command-line text editor, e.g. `vi`  (if your not familiar with `vi` type "nano" instead of "vi" - nano is less adanced yet easier to use) 
```
sudo vi /etc/iptables/rules.v4
```

4. Now type the following in the editor, save and exit.

```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT
COMMIT
```

5. Edit IPv6 rules
```
sudo vi /etc/iptables/rules.v6
```

6. Now type the following in the editor, save and exit.

```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT DROP [0:0]
COMMIT
```

7. Edit **/etc/default/keyboard** (When attaching with Monitor and a US Keyboard, you may find that your not able to type things like "|". This is not a problem when going over SSH.)

Replace 
```
XKBMODEL="pc105"
XKBLAYOUT="gb"
```
with
```
XKBMODEL="pc104"
XKBLAYOUT="us"
```

8. Reboot:
```
sudo reboot
```

-- start of citical section (complete until the end of critical section or remove from netwrok before rebooting) ---

9. Now run:

```
cat /etc/iptables/rules.v4 | sudo iptables-restore
cat /etc/iptables/rules.v6 | sudo iptables-restore -6
```

Now the output of `sudo iptables-save` should look like the lines in step 4:

 * numbers at the end of the line may be different, those are your network statistics
 
10. Changed the password. Run `sudo raspi-config`. Select: **Change Password** If you don't change the password you'll get hacked.
11. Connect enthernet cable or (Optionally) [setup Wi-Fi](https://github.com/alevchuk/minibank/blob/first/other-notes/wifi.md)
12. Update the system: `sudo apt update && sudo apt upgrade;`. If you don't upgrade you'll get hacked.
13. Make firewall persistent:
```
sudo apt install iptables-persistent  # when asked "Save currrent rules?" say "Yes" for both IPv4 and IPv6

sudo /etc/init.d/netfilter-persistent restart

sudo iptables-save  # show current v4 rules: check if this just like before
sudo iptables-save -6  # show current v6 rules: check that it is drop-everything 
```

14. Reboot Pi
```
sudo reboot
```

15. Again check firewall after reboot:
```
sudo iptables-save  # show current v4 rules: check if this just like before
sudo iptables-save -6  # show current v6 rules: check that it is drop-everything 
```

-- end of citical section ---



16. SSH over Tor

If you want still to SSH over the local network (without Tor) you can do this:  https://github.com/alevchuk/minibank/blob/first/other-notes/no-tor-ssh.md and skip steps 16 thru 22.

```
sudo apt install tor
```


17. Enable remote login over SSH. Run `raspi-config` select **Interface Options -> SSH -> SSH server to be enabled**

18. Test ssh locally (ssh to yourself while in Keyboard-Monitor mode):
```
ssh 127.0.0.1
```

19. Configure Tor

```
sudo vi /etc/tor/torrc
```
Find and uncomment lines with:
```
HiddenServiceDir
HiddenServicePort
```
and change
```
HiddenServicePort 80 127.0.0.1:8080
```
to
```
HiddenServicePort 22 127.0.0.1:22
```

and add another line
```
HiddenServiceVersion 3
```

20. Restart Tor
```
sudo systemctl restart tor@default.service
```

21. Reveal the hidden hostname
```
cat /var/lib/tor/hidden_service/hostname
```
write it down in a safe place


22. From your laptop run: `torify ssh pi@HOSTNAME_HERE.onion` enter your new password

23. Follow [Authorized Keys](#authorized-keys) section

### Remote Login (AWS node)

If your seting up Raspberry Pi node **home node** then skip this section and proceed to **Remote Login (Home node)**.

AWS has a default firewall setup for you. You can manage it from the Amazon AWS web console under Security Groups. Yet, to be sure your in control, you should also setup a local firewall.

NOTE: In this setup it's easy to make a mistake and get locked out of the remote server, so I recomend takeing a snapshot of the root-drive in AWS at this point in time.


```
sudo apt update
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

8. From your laptop, use the IP from step 5 and run: `ssh pi@YOUR_IP_HERE` enter your new password

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

Once you can login without a password, disable login with password: edit `/etc/ssh/sshd_config` and find PasswordAuthentication. Uncommented and set to no. Restart ssh server `sudo systemctl restart ssh`

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

### Lookup storage device info

In this sections were going to look up the following for each of the SSDs:
* Block device name (e.g. "sda")
* idVendor (a hex number, e.g. "04e8")
* idProduct (a hex number, e.g. "61f5")

Steps:
1. Run `sudo dmesg --follow`
2. Un-plung and re-plug one of the external SSD drives
3. Look for the block device name, starting with "sd" followed by a lowercase english letter. Write that down.
4. Look for idVendor and idProduct. Write those down
5. Repeate from step 2 for the other SSD

NOTE: it's important to label the storage devices with their idVendor and idProduct in case one of them fails and you'll need to know which one to replace. Block device names change depending in which order you plug in the drives. For that reasob, **do not write the block device name (the "sd" followed by a letter) on the lable**.

From now I will refer to the block device names as:
* YOUR_SSD_BLOCK_DEVICE_1 ("sd" followed by a letter)
* YOUR_VENDOR_ID_FOR_DEVICE_1 (hex number)
* YOUR_PRODUCT_ID_FOR_DEVICE_1 (hex number)
* and the above 3 for DEVICE_2

The relevant output of `dmesg --follow` would look like this:
```
[22341.090044] usb 2-1: new SuperSpeed Gen 1 USB device number 3 using xhci_hcd
[22341.118242] usb 2-1: New USB device found, idVendor=04e8, idProduct=61f5, bcdDevice= 1.00
[22341.118261] usb 2-1: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[22341.118273] usb 2-1: Product: Portable SSD T5
[22341.118284] usb 2-1: Manufacturer: Samsung
[22341.118296] usb 2-1: SerialNumber: 1234567DAFFD
[22341.136371] scsi host3: uas
[22341.139726] scsi 3:0:0:0: Direct-Access     Samsung  Portable SSD T5  0    PQ: 0 ANSI: 6
[22341.143092] sd 3:0:0:0: [sdd] 976773168 512-byte logical blocks: (500 GB/466 GiB)
[22341.143406] sd 3:0:0:0: [sdd] Write Protect is off
[22341.143420] sd 3:0:0:0: [sdd] Mode Sense: 43 00 00 00
[22341.144983] sd 3:0:0:0: [sdd] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[22341.145925] sd 3:0:0:0: Attached scsi generic sg2 type 0
[22341.147078] sd 3:0:0:0: [sdd] Optimal transfer size 33553920 bytes
[22341.174323] sd 3:0:0:0: [sdd] Attached SCSI disk
```
* Notice that `[sdd]` is the block device name in the above example

### Disable UAS

To prevent occasinal freezing of your Pi, disable UAS. UAS (USB Attached SCSI) is a need protocal that adds marginal performance improvement yet it's not reliable (at lease for the current USB 3.0 hardware of the RasberryPi). I suspect that the freezes get triggered by radio interferance of UBS 3.0 with 2.4 GHz Wi-Fi or Bluetooth. However, the old mass storage device protocal is resilient to this issue. So we simply need to follow Rapberry Pi team's recomendation and disable UAS.

From my tests, the following were the adanates of disabling UAS:
* The freezes stopped.
  * By freeze I mean: geting /mnt/btrfs mount point failure with "uas_eh_abort_handler" for "CMD OUT" and "CMD IN" errors in `dmesg` 
  * The failure does not cause data loss/corruption, yet brings down the whole system
  * A repro is to try to run `btrfs balance start /mnt/btrfs` and you'll get the failure within a minute
* For the first time I'm now able to run and compleate `sudo btrfs balance start -v --full-balance /mnt/btrfs/`
* There is no significant performance degradations from disabling UAS

For more details on this issue see https://github.com/alevchuk/minibank/blob/first/incidents/i5-ssd-disconnect.md

To check if you have UAS enabled:
1. run `dmesg | grep -v registered | grep uas` soon after rebooting the Pi 
2. You should see "scsi host0: uas"

To disable UAS:
1. From previous section you'll need the idVendor/idProduct pairs for both SSD devices
2. If you already setup /mnt/btrfs then stop all services using it and run `umount /mnt/btrfs`
3. Make a backup `sudo cp /boot/cmdline.txt /cmdline.txt-old-backup`
4. Edit the boot command by running `sudo vi /boot/cmdline.txt`
5. Add `usb-storage.quirks=YOUR_VENDOR_ID_FOR_DEVICE_1:YOUR_PRODUCT_ID_FOR_DEVICE_1:u,YOUR_VENDOR_ID_FOR_DEVICE_2:YOUR_PRODUCT_ID_FOR_DEVICE_2:u ` in front of the command
  * it's "usb-storage.quirks=" followed a comman separated list of "idVendor:idProduct:u"
  * The part that you add needs to be followed by a space " " (e.g. `usb-storage.quirks=0781:558c:u,04e8:61f5:u dwc_otg.lpm_enable=0 console=serial0,115200 ...`)
  * replace YOUR_...
  * don't miss the ":u" at the end
  * The whole line should look similar to this `usb-storage.quirks=0781:558c:u,04e8:61f5:u dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=3acd0083-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`
6. Reboot your pi
7. Run `dmesg | grep UAS` (if you see "usbcore: registered" then that's OK, it case be registered yet still disabled) and verify that it mentions blocklisting/disabling of UAS.

### BTRFS RAID-1 Mirror

Install BTRFS progs:
```
sudo apt update
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
sudo umount /mnt/btrfs
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

2. Follow instruction to build bitcoin: [alevchuk/minibank/bitcoin](https://github.com/alevchuk/minibank/tree/first/bitcoin)


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

### prune=0  # No prune if you have 1 TB drive(s)
prune=476000  # we have 500 TB of storage space (raid-1 of 2 drives 500 TB each) 

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

### Convenience stuff

While your bitcoin chain syncs...

Skip the following sections if your setting up a node on Amazon AWS or Google cloud:
* Name your Pi
* Time-zone
* Non-British Keyboard

#### Name your Pi

Give your host a name. Put what you want instead of "minibank1"
```
sudo hostname minibank1
```

Edit 2 files replacing "raspberrypi" with the name you came up with. No spaces or punctuation.
```
sudo vi /etc/hostname
sudo vi /etc/hosts  # edit the line with 127.0.0.1 adding a space and your new hostname at the end of that line

sudo vi /etc/cloud/templates/hosts.debian.tmpl  # do the same as for  /etc/hosts  
# yet if this file does not exist then skip this step.
# don't rely on the {{hostname}} sytax (it will not do what you most likely expect),
# instead add a space and the new hostname at the end, after "{{hostname}} "
```

you'll see the change after rebooting, run sudo reboot, re-SSH back in run `sudo mount /mnt/btrfs/` and resume the chain sync:
```
sudo su -l bitcoin
bitcoind
```

#### Time-zone


Run `raspi-config` and select **Localization Options --> Change Timezone** to make your system clock right. Check time by running `date`




#### bash-completion

```
sudo apt update
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

Python IDE:
```
sudo su -c "cat <<EOF >> /etc/vim/vimrc
set paste
syntax on
set tabstop=4 shiftwidth=4 expandtab
EOF
"
```

#### Bash

To the end of the bash rc file add the following lines after running `vi ~/.bashrc`
```
# https://unix.stackexchange.com/a/48113/4058
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it
# Save and reload the history after each command finishes
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
```

Now do the same /etc/skel by running `sudo vi /etc/skel/.bashrc`
* so that every new accounts gets this

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

[Bitcoin]
bitcoin.active=1
bitcoin.mainnet=1
bitcoin.node=bitcoind

[Bitcoind]
bitcoind.zmqpubrawblock=tcp://localhost:29000
bitcoind.zmqpubrawtx=tcp://localhost:29001
bitcoind.rpchost=localhost
bitcoind.rpcuser=$$PASSWORD_1_HERE$$ 
bitcoind.rpcpass=$$PASSWORD_2_HERE$$ 

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
lnd
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

### Open LND port on your router

In your minibank, to `/etc/iptables/rules.v4` add:
```
# Allow LND peers
-A INPUT -p tcp --dport 9735 -j ACCEPT
```
and run 
```
sudo /etc/init.d/netfilter-persistent restart
```

If this is on AWS then also update the Secutrity Group in AWS web console.

In your home router, forward the port 9735 to the host running LND. Here is [a guide](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) on how to do that.

Test with netcat (nc) from a different host. Use onion addresses (e.g. z123zxczxc87z6xc6zx87c6zxc876zxxyz.onion):
```
seq 100 | torify nc -v <onion_address> 9735
```

lnd logs will show
```
2018-01-08 20:41:07.856 [ERR] BTCN: Can't accept connection: unable to accept connection from ...
```
- this error is good. it means the netword delivered the packets. error is expected because the packet is malformed.

### Install LND operations scripts

Change into Lighting account:
```
sudo su -l lightning
```

Checkout scripts and copy to `lnd-e2e-testing`:
```
cd ~
git clone https://github.com/alevchuk/minibank.git
cp -r ~/minibank/scripts/* ~/lnd-e2e-testing/
```

* close_channel_custom.py
* pay_or_get_paid.py
* rebalance_channels.py
* treasury_report.py

Most of those scripts are short/readable and have internal documentation.



### Keep track of your total balance

Use [treasury_report.py script](scripts/treasury_report.py)
```
# One-time setup:
~/lnd-e2e-testing/treasury_report.py >> ~/balance_history.tab

# Track balance
while :; do echo; (cat ~/balance_history.tab; ~/lnd-e2e-testing/treasury_report.py ) | column -t; date; sleep 60; done

# Record balance
~/lnd-e2e-testing/treasury_report.py | grep -v Time  >> ~/balance_history.tab
```

As channels open and close you may see total balance go down but should it recover eventually. That's because LND overestimates the fees for the channel closing transactions.



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
ln -s /mnt/btrfs/lightning/src/ ~/src_readonly
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
${GOPATH-$HOME/go}/src/github.com/prometheus/node_exporter/node_exporter --no-collector.mdadm --no-collector.infiniband
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

#### LND metrics

Install pip
```
sudo apt install python3-pip
```

Vitrualenv is the only pip package that you will need to install system-wide. Everything else will be installed locally home directories called virtual environments.
```
sudo pip3 install virtualenv
```

Setup
```
sudo su -l lightning
git clone https://github.com/alevchuk/minibank.git minibank/
cd minibank
git pull

mkdir ~/lnd-e2e-testing
cp scripts/liquidity_mon.py ~/lnd-e2e-testing/

cd ~/lnd-e2e-testing/
virtualenv --python=python3.7 monitoring-env
cd monitoring-env
. ./bin/activate
pip3 install prometheus_client
deactivate
```

Run liquidity_mon
```
( cd ~/lnd-e2e-testing/ && . ./monitoring-env/bin/activate && ./liquidity_mon.py )
```

Test
```
curl localhost:6549
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

To install and run Grafana follow [alevchuk/minibank/grafana](https://github.com/alevchuk/minibank/blob/first/grafana/README.md)

![alt text](https://raw.githubusercontent.com/alevchuk/minibank/first/img/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")



# Operations

This section is planned

For now, use [BTRFS Raid wiki](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices#Adding_new_devices)

