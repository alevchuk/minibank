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

1. Setup no-incoming-connections firewall **before connecting to the network!** If you don't add a firewall you'll get hacked:

Run:
```
sudo mkdir /etc/iptables
```

2. Edit /etc/iptables/rules.v4 with your favourite command-line text editor, e.g. `vi`  (if your not familiar with `vi` type "nano" instead of "vi" - nano is less advanced yet easier to use) 
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

-- start of critical section (complete until the end of critical section or remove from network before rebooting) ---

9. Now run:

```
cat /etc/iptables/rules.v4 | sudo iptables-restore
cat /etc/iptables/rules.v6 | sudo iptables-restore -6
```

Now the output of `sudo iptables-save` should look like the lines in step 4:

 * numbers at the end of the line may be different, those are your network statistics
 
10. Changed the password. Run `sudo raspi-config`. Select: **Change Password** If you don't change the password you'll get hacked.
11. Connect Ethernet cable or (Optionally) [setup Wi-Fi](https://github.com/alevchuk/minibank/blob/first/other-notes/wifi.md)
12. Update the system: `sudo apt update && sudo apt upgrade;`. If you don't upgrade you may get hacked. Some keyboards stop working after upgrade so be ready to find a different keyboard (DAS Keyboard works well, yet Pi needs to be rebooted while it's plugged in).
13. Make firewall persistent, if you don't persist firewall you may get hacked:
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

-- end of critical section ---



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

24. Once Authorized Keys are working, disable SSH login with password https://docs.joinmastodon.org/admin/prerequisites/#do-not-allow-password-based-ssh-login-keys-only


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


