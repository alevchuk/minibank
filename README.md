# minibank
bitcoin lightning node

![model 4](https://raw.githubusercontent.com/alevchuk/minibank/first/img/minibank-2020-04-10.jpg "minibank model 4, Pi 4, 4 GB RAM, 500GB SSD, running mainnet LND")

For older models see [History](https://github.com/alevchuk/minibank/blob/first/other-notes/HISTORY.md).

Table of contents
=================

  * [About](#about)
  * [Hardware](#hardware)
  * [Operating System](#operating-system)


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
* SAMSUNG 1 TB SSD (for datat; Raid-1 mirror): [SAMSUNG T7 Portable SSD 1TB](https://camelcamelcamel.com/product/B0874YJP92)
* SanDisk 1 TB SSD (for data; Raid-1 mirror): [SanDisk 1TB Extreme Portable External SSD](https://camelcamelcamel.com/product/B078STRHBX)
  * **Pros:** Different manufacturers so they don't fail at the same time. **Cons:** SanDisk failed first after I used this setup for several year. SanDisk company only tests Win and Mac. It does not show having cache on Linux so this many be a result of degraded perfromance. No indicator light. Shipping took much longer than SAMSUNG. **Conclusion:** in the future I might just get two SAMSUNGs instead


Hardware with known issues:
* [Not sure this is still ture. Now I know the data corruption is caused by UAS. So later in this article I disable UAS. This may actually fix the percieved Seagate issue] WARNING: The following Seagate divice [may] caused data corruption when pluging into USB, other storage connected to UBS also got affected. DO NOT USE Seagate 500 GB SSD (for Raid-1 mirror): [Seagate-Barracuda-500GB-External-Portable](https://camelcamelcamel.com/product/B083FF3PJ9)



## Operating System

1. Download the image the Raspberry Pi Foundation’s official supported operating system
**Raspberry Pi OS (64-bit) Lite** from [official raspberrypi link](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-64-bit)
2. Uncompress the file: `xz -d Downloads/2023-05-03-raspios-bullseye-arm64-lite.img.xz`
3. Transfer the contents on the ".img" file to your SD card (I use `dd`, Raspberry Pi has installers and instcutions for doing this from [Linux](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md), [Mac](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md), and [Windows](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md)) Here is how I do it (avoiding using Rasberry Pi Installer):
```
sudo dmesg --follow  # first run the command then insert your SD card and verify that it's sdb
# Press Ctrl-c to exist out of dmesg or run in a different terminal / tab
sudo dd if=Downloads/2023-05-03-raspios-bullseye-arm64-lite.img of=/dev/sdb  # careful, sdb may be some other drive, check dmesg for correc block device
```


### Create your username in Raspberry Pi

Now that you have the SD card, put it in, and connect the Pi to a Monitor and a keyboard.

On first boot, the Pi will ask you to create an account. Give it your special username and a strong password.

