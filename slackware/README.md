NOTE: work in progress, starting 2020-09-12


# install Slackware

## follow official instructions

https://docs.slackware.com/howtos:hardware:arm:raspberrypi4

1. A small modification to the script for putting Slackware ARM mini root file system in the SD Card:
```
#!/bin/bash

set -e
set -o
set -u
set -x


wget -c ftp://ftp.arm.slackware.com/slackwarearm/slackwarearm-devtools/minirootfs/roots/slack-14.2-miniroot_01Jul16.tar.xz
mkdir -p ~/mnt
mount /dev/sda2 ~/mnt
tar -C ~/mnt -xf slack-14.2-miniroot_01Jul16.tar.xz
echo "/dev/sda2 /boot vfat defaults 0 0" | sudo tee ~/mnt/etc/fstab
echo "/dev/sda2 /     ext4 defaults 0 0" | sudo tee -a ~/mnt/etc/fstab
echo "proc           /proc proc defaults 0 0" | sudo tee -a ~/mnt/etc/fstab
PASSWD=$(openssl passwd -1 -salt cetkq/enZx6/c2 password_goes_here)
sed -i "s|\(root:\).*\(:16983:0:::::\)|\1${PASSWD}\2|" ~/mnt/etc/shadow
sed -i 's|USE_DHCP\[1\]=""|USE_DHCP\[1\]="yes"|' ~/mnt/etc/rc.d/rc.inet1.conf
echo "PermitRootLogin yes" | sudo tee -a ~/mnt/etc/ssh/sshd_config
umount ~/mnt
```

2. Set the temparary password (PASSWD) to something unique for good measure.
