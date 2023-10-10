# minibank
bitcoin lightning node

![model 4](https://raw.githubusercontent.com/alevchuk/minibank/first/img/minibank-2020-04-10.jpg "minibank model 4, Pi 4, 4 GB RAM, 500GB SSD, running mainnet LND")

For older models see [History](https://github.com/alevchuk/minibank/blob/first/other-notes/HISTORY.md).

Table of contents
=================

  * [About](#about)
  * [Hardware](#hardware)
  * [Operating System](#operating-system)
  * [Heat](#heat)
  * [Network](#network)
  * [Storage](#storage)
  * [Software](#software)


## About

Minibank is a HOWTO for building a Lightning Network node from scratch
* Limited set of features: bitcoind, lnd, tor, electrs
* Components are built from source code
* Mirror Raid with 2 external storage devices
* Development environment (CLI only)
* Monitoring (time series, dashboards, alerts)

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

### Model 4B :: Node at Home

Pi 4 Model B. Two high-speed SSDs for Raid-1 mirroring.

Total **317 USD** as of Oct 2023

* Pi 4b kit (8GB RAM): [Raspberry Pi 4 8GB Model B](https://camelcamelcamel.com/product/B0B6ZJGF4Q)
* Power supply
* FLIRC Passive cooling case [Flirc Raspberry Pi 4 Case](https://camelcamelcamel.com/Flirc-Raspberry-Pi-Case-Silver/product/B07WG4DW52)
* Micro SD card 32G (for operating system) [SanDisk-Extreme-microSD-UHS-I-Adapter](https://camelcamelcamel.com/product/B06XWMQ81P)
* Card Reader (for 1 time setup) [Transcend-microSDHC-Reader-TS-RDF5K-Black](https://camelcamelcamel.com/Transcend-microSDHC-Reader-TS-RDF5K-Black/product/B009D79VH4)
* SAMSUNG 1 TB SSD (for data; Raid-1 mirror): [SAMSUNG T7 Portable SSD 1TB](https://camelcamelcamel.com/product/B0874YJP92)
* SanDisk 1 TB SSD (for data; Raid-1 mirror): [SanDisk 1TB Extreme Portable External SSD](https://camelcamelcamel.com/product/B078STRHBX)
  * **Pros:** Different manufacturers so they don't fail at the same time. **Cons:** SanDisk failed first after I used this setup for several year. SanDisk company only tests Win and Mac. It does not show having cache on Linux so this many be a result of degraded performance. No indicator light. Shipping took much longer than SAMSUNG. **Conclusion:** in the future I might just get two SAMSUNG drives instead


Hardware with known issues:
* [Not sure this is still true. Now I know the data corruption is caused by UAS. So later in this article I disable UAS. This may actually fix the perceived Seagate issue] WARNING: The following Seagate device [may] caused data corruption when plugging into USB, other storage connected to UBS also got affected. DO NOT USE Seagate 500 GB SSD (for Raid-1 mirror): [Seagate-Barracuda-500GB-External-Portable](https://camelcamelcamel.com/product/B083FF3PJ9)



## Operating System

1. Download the image the Raspberry Pi Foundation’s official supported operating system
**Raspberry Pi OS (64-bit) Lite** from [official raspberrypi link](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-64-bit)
2. Uncompress the file: `xz -d Downloads/2023-05-03-raspios-bullseye-arm64-lite.img.xz`
3. Transfer the contents on the ".img" file to your SD card (I use `dd`, Raspberry Pi has installers and instructions for doing this from [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md), [Mac](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md), and [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md)) Here is how I do it (avoiding using Raspberry Pi Installer):
```
sudo dmesg --follow  # first run the command then insert your SD card and verify that it's sdb
# Press Ctrl-c to exist out of dmesg or run in a different terminal / tab
sudo dd if=Downloads/2023-05-03-raspios-bullseye-arm64-lite.img of=/dev/sdb  # careful, sdb may be some other drive, check dmesg for correc block device
```


### First Login (create your username in Raspberry Pi)

Now that you have the SD card, put it in. Don't connect to network. Connect monitor and keyboard. Power-up Pi.


On first boot, the Pi will ask you to create an account. Give it your special username and a strong password.

Once logged in, check to make sure you have a 64-bin linux OS, type:
```
arch
```
if you get "arch64" you're good to go (continue with this manual). Otherwise, this manual will not work (maybe you have have older hardware that's 32-bit only or you downloaded the wrong SD card image).

## Heat

I recommend using FLIRC passive cooling:
- Pi temp under 50C
- No more worries of airflow obstruction
- Fan won't fail because there is not fan

If you still want to go with a fan, follow [this howto](https://blog.hackster.io/do-you-need-to-use-a-fan-for-cooling-with-the-new-raspberry-pi-4-6d523ca12453). Tip: Connect the fan to GPIO pins with quiet cooling mode works best for me https://www.raspberrypi.org/forums/viewtopic.php?t=248918#p1519636

To measure the temperature, run:
```
while :; do /opt/vc/bin/vcgencmd measure_temp; sleep 1; done
```

Anything bellow 70C is good. The throttling [kicks in at 80 C](https://www.theregister.co.uk/2019/07/22/raspberry_pi_4_too_hot_to_handle/).

## Network

Don't connect to network yet.

Connect via monitor and keyboard.

The following ~20 steps will need to be typed (not copy and pasted) because we are connected directly without network (not thru another computer). Setting up the firewall this way provides a higher level of security.

Tip: take a photo of these instructions and open it on your phone next to your keyboard

1. Setup no-incoming-connections firewall **before connecting to the network!** If you don't add a firewall you're at risk of getting hacked:

Run:
```
sudo mkdir /etc/iptables
```

2. Edit /etc/iptables/rules.v4 with your favourite command-line text editor, e.g. `vi`  (if your not familiar with `vi` type "nano" instead of "vi" - nano is less advanced yet easier to use) 
```
sudo vi /etc/iptables/rules.v4
```

3. nothing

4. Now type the following in the editor, save and exit.

```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -i lo -j ACCEPT
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


7. Reboot:
```
sudo reboot
```

-- start of critical section (this section contains the step of connecting to the network, complete until the end of critical section or remove from network before rebooting) ---

8. Now run:

```
sudo iptables -F
sudo ip6tables -F
cat /etc/iptables/rules.v4 | sudo iptables-restore
cat /etc/iptables/rules.v6 | sudo ip6tables-restore
```

9. Carefully check for duplicate lines or extra lines in the output of:
```
sudo iptables-save  # should look exactly like the lines in step 4
sudo ip6tables-save  # should look exactly like the lines in step 6
```
 * numbers at the end of the line may be different, those are your network statistics (if you accidentally connected to the network then the dropped/accepted packets will get counted)
 * if you see entries that don't match what you head in step 4 and 6, go back and check that rules were typed in correctly
 
10. Connect Ethernet cable or (Optionally) [setup Wi-Fi](https://github.com/alevchuk/minibank/blob/first/other-notes/wifi.md)

NOTE: steps 9 (check firewall) and 10 (connect to network) need to be done back to back. E.g. if you reboot firewall rules will be lost and you'll need to go back to step 8 before connecting to network.

     
11. Update the system: `sudo apt update && sudo apt upgrade;`. If you don't upgrade you may get hacked. Some keyboards stop working after upgrade so be ready to find a different keyboard (DAS Keyboard works well, yet Pi needs to be rebooted while it's plugged in).
11. Make firewall persistent, if you don't persist firewall you may get hacked:
```
sudo apt install iptables-persistent  # when asked "Save currrent rules?" say "Yes" for both IPv4 and IPv6

sudo /etc/init.d/netfilter-persistent restart

sudo iptables-save  # show current v4 rules: check if this just like before
sudo iptables-save -6  # show current v6 rules: check that it is drop-everything 
```

12. Disconnect from network (Ethernet cable or Wi-Fi)
13. Reboot Pi
```
sudo reboot
```

14. Again check firewall after reboot:
```
sudo iptables-save  # show current v4 rules: check if this just like before
sudo ip6tables-save  # show current v6 rules: check that it is drop-everything 
```

15. Connect to network (Ethernet cable or Wi-Fi)

-- end of critical section ---



16. SSH over Tor

We first setup a management connection over Tor which will be slow. Later you will be able to add a fast management connection on your local network.

Tor:
- slow
- do not need to know any IPs
- accessible from anywhere on the internet with a Tor client

Local network:
- fast
- need to know local IP of the Raspberry Pi
- accessible only when you're connected to your local network

```
sudo apt install tor
```


17. Enable remote login over SSH. Run `sudo raspi-config` and select **Interface Options -> SSH -> SSH server to be enabled**

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


22. From your laptop run: `torify ssh <PI_USER_NAME>@<TOR_HOSTNAME_HERE>.onion` (replace <PI_USER_NAME> from "First Login" section, and <TOR_HOSTNAME_HERE> from step 21). When prompted enter your Raspberry Pi password from "First Login" section.

23. I recommend that you also setup a fast SSH over the local network (without Tor) you can do this by following https://github.com/alevchuk/minibank/blob/first/other-notes/no-tor-ssh.md
  

24. Follow [Authorized Keys](#authorized-keys) section



### Authorized keys

So you don't have to type the password every time you need to log-in to the pi, setup authorized_keys.

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
cat >> ~/.ssh/authorized_keys
```
paste the pubkey from clipboard, press Enter, and then press Ctrl-d.

Now run:
```
chmod o=,g= ~/.ssh/authorized_keys
```
Now log out, press Ctrl-d.

Now try logging back in like this:
```
torify ssh -i ~/.ssh/minibank_id_rsa <PI_USER_NAME>@<TOR_HOSTNAME_HERE>.onion
```
You should not need to re-enter password.

Once you can login without a password, disable login with password: edit `/etc/ssh/sshd_config` and find PasswordAuthentication. Uncommented and set to no. Restart ssh server `sudo systemctl restart ssh`

Finally, back on your laptop, add an alias
```
echo 'alias mb4="torify ssh -i ~/.ssh/minibank_id_rsa <PI_USER_NAME>@<TOR_HOSTNAME_HERE>.onion"' >> ~/.bash_profile
. ~/.bash_profile
```

Now type `mb4` and that should log you into the Pi.


## Storage

In this section will setup a Raid-1 Mirror from your two new SSD drives.

WARNING: any data in the SSD drives will be deleted.

### Lookup storage device info

In this sections were going to look up the following for each of the SSDs:
* Block device name (e.g. "sda")
* idVendor (a hex number, e.g. "04e8")
* idProduct (a hex number, e.g. "61f5")

Steps:
1. Run `sudo dmesg --follow`
2. Unplug and re-plug one of the external SSD drives
3. Look for the block device name, starting with "sd" followed by a lowercase English letter. Write that down.
4. Look for idVendor and idProduct. Write those down
5. Repeat from step 2 for the other SSD

NOTE: it's important to label the storage devices with their idVendor and idProduct in case one of them fails and you'll need to know which one to replace. Block device names change depending in which order you plug in the drives. For that reason, **do not write the block device name (the "sd" followed by a letter) on the label**.

From now I will refer to the block device names as:
* YOUR_SSD_BLOCK_DEVICE_1 ("sd" followed by a letter)
* YOUR_VENDOR_ID_FOR_DEVICE_1 (hex number)
* YOUR_PRODUCT_ID_FOR_DEVICE_1 (hex number)
* and same for DEVICE_2

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

To prevent occasional freezing of your Pi, disable UAS. UAS (USB Attached SCSI) is a protocol that adds marginal performance improvement yet it's not reliable (at least for the current USB 3.0 hardware of the RaspberryPi). I suspect that the freezes get triggered by radio interference of USB 3.0 with 2.4 GHz Wi-Fi or Bluetooth. However, the old mass storage device protocol is resilient to this issue. So we simply need to follow the Raspberry Pi team's recommendation and disable UAS.

From my tests, the following were the advantages of disabling UAS:
* The freezes stopped.
  * By freeze I mean: getting /mnt/btrfs mount point failure with "uas_eh_abort_handler" for "CMD OUT" and "CMD IN" errors in `dmesg`
  * The failure does not cause data loss/corruption, yet brings down the whole system
  * A repro is to try to run `btrfs balance start /mnt/btrfs` and you'll get the failure within a minute
* For the first time I'm now able to run and complete `sudo btrfs balance start -v --full-balance /mnt/btrfs/`
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
  * it's "usb-storage.quirks=" followed a comma separated list of "idVendor:idProduct:u"
  * The part that you add needs to be followed by a space " " (e.g. `usb-storage.quirks=0781:558c:u,04e8:61f5:u dwc_otg.lpm_enable=0 console=serial0,115200 ...`)
  * replace YOUR_...
  * don't miss the ":u" at the end
  * The whole line should look similar to this `usb-storage.quirks=0781:558c:u,04e8:61f5:u dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=3acd0083-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`
6. Reboot
7. Check `dmesg | less`. Search for "UAS", by typing "/UAS" and pressing "n" to go to next one. There should be 2 "UAS is ignored" messages for each USB device. They look like this:
```
[    1.617927] usb 2-1: UAS is ignored for this device, using usb-storage instead
[    1.618064] usb 2-1: UAS is ignored for this device, using usb-storage instead
...
[    2.049009] usb 2-2: UAS is ignored for this device, using usb-storage instead
[    2.049152] usb 2-2: UAS is ignored for this device, using usb-storage instead
...
[    2.624504] sd 0:0:0:0: [sda] 1953525168 512-byte logical blocks: (1.00 TB/932 GiB)
...
[    3.071842] sd 1:0:0:0: [sdb] 976773168 512-byte logical blocks: (500 GB/466 GiB)
```

### BTRFS RAID-1 Mirror

Install BTRFS progs:
```
sudo apt update
sudo apt install btrfs-progs
```

WARNING: any data in the SSD drives will be deleted. If you don't know what your doing, try running the command without `--force` first.

Create file-systems Bitcoin and LND nodes
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

Follow instruction to build bitcoin: [alevchuk/minibank/bitcoin](https://github.com/alevchuk/minibank/tree/first/bitcoin)


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
disablewallet=0

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

rpccookiefile=/home/bitcoin/bitcoinclients/cookie


# Listen for RPC connections on this TCP port:
####rpcport=8332

onlynet=ipv4
zmqpubrawblock=tcp://0.0.0.0:29000
zmqpubrawtx=tcp://0.0.0.0:29001

prune=0  # No prune if you have 1 TB drive(s)
## prune=476000  # if you have 500 TB of storage space (raid-1 of 2 drives 500 TB each) you'll need to prune but you will need to disable txindex and blockfilterindex

txindex=1  # Maintain a full transaction index, LND uses this, otherwise there will be a lot of disk scans
blockfilterindex=1 #  takes a few GB of storage and helps to speed-up blockchain rescanning

## # tunning (not needed on the new Pi3 with SSDs)
## dbcache=200  # Maximum database cache size <n> MiB
## maxorphantx=10  # Keep at most <n> unconnectable transactions in memory (default: 100)
## maxmempool=50  # Keep the transaction memory pool below <n> megabytes
## maxconnections=20  # Maintain at most <n> connections to peers
## maxuploadtarget=50  # MiB/day for the community
## whitelist=download@127.0.0.1  # disable the limit for local p2p connections

# Detailed logging
####debug=bench
####debug=db
####debug=reindex
####debug=cmpctblock
####debug=coindb
####debug=leveldb
```

