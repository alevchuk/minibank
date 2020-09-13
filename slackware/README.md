# Minibank on Slackware

NOTE: work in progress, doc started on 2020-09-12

Instructions on how to install the same hardware and software as https://github.com/alevchuk/minibank yet on Slackware operating system. The adavantage of Slackware is it's design phelosophy of keeping packages simple with as little modifications to upstream as possible.


Minibank currently uses the Rasbian operating system, however setting it up on Slackware would provide several advantages:
- Native 64-bit operating system
- No middleman for OS distribution (Debian -> Rasbian) - reduces changes of supply chain attacks
- Focus on simplicity. E.g. less packages and less changes, resulting in a smaller to [Slacker Security Advisory](http://www.slackware.com/security/list.php?l=slackware-security&y=2020) as compared to [Debian Security Advisory](https://www.debian.org/security/2020/)


## Install Slackware (without a Raspbian image)

Follow official instructions: https://docs.slackware.com/howtos:hardware:arm:raspberrypi4#manual_install_method_without_a_raspbian_image

Here are small modification to the script that makes things safer (by using /dev/sda2 instaed your root disk, enable error checking in bash)
 
* In step 2 (Put the Raspberry Pi firmware in the SD Card):
```bash
#!/bin/bash

set -e
set -o
set -u
set -x

mkdir -p ~/mnt

git clone https://github.com/raspberrypi/firmware.git
sudo mount /dev/sda1 ~/mnt
sudo cp -r firmware/boot/* ~/mnt
sudo umount ~/mnt
sudo mount /dev/sda2 ~/mnt
sudo mkdir -p ~/mnt/lib/modules
sudo cp -r firmware/modules/* ~/mnt/lib/modules
sudo umount ~/mnt
```


* In step 3 (putting Slackware ARM mini root file system in the SD Card),:
  1. Set the temparary password (PASSWD) to something unique for good measure.
```bash
#!/bin/bash

set -e
set -o
set -u
set -x

mkdir -p ~/mnt

wget -c ftp://ftp.arm.slackware.com/slackwarearm/slackwarearm-devtools/minirootfs/roots/slack-14.2-miniroot_01Jul16.tar.xz
sudo mount /dev/sda2 ~/mnt
sudo tar -C ~/mnt -xf slack-14.2-miniroot_01Jul16.tar.xz
echo "/dev/mmcblk0p1 /boot vfat defaults 0 0" | sudo tee ~/mnt/etc/fstab
echo "/dev/mmcblk0p2 /     ext4 defaults 0 0" | sudo tee -a ~/mnt/etc/fstab
echo "proc           /proc proc defaults 0 0" | sudo tee -a ~/mnt/etc/fstab
PASSWD=$(openssl passwd -1 -salt cetkq/enZx6/c2 temporary_password_goes_here)
sudo sed -i "s|\(root:\).*\(:16983:0:::::\)|\1${PASSWD}\2|" ~/mnt/etc/shadow
sudo sed -i 's|USE_DHCP\[1\]=""|USE_DHCP\[1\]="yes"|' ~/mnt/etc/rc.d/rc.inet1.conf
echo "PermitRootLogin yes" | sudo tee -a ~/mnt/etc/ssh/sshd_config
sudo umount ~/mnt
```
