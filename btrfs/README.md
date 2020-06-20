# Latest release of BTRFS on Raspberry Pi


## Step 1: Upgrade Kernel and Firmware

Note your kernel version before
```
uname -a
```

Simply run `rpi-update`
to read more how this works or how to Revert see https://www.raspberrypi.org/documentation/linux/kernel/updating.md

Reboot the Pi
```
reboot
```

Note your kernel version after
```
uname -a  # should print "4.19.42+" or greater
```

## Step 2: Build and install btrfs-progs (userspace utilities)


Install dependencies
```
sudo apt-get install libuuid1 libblkid-dev liblzo2-dev zlibc libzstd-dev python-setuptools python3-setuptools
```
original list of dependencies is here https://github.com/kdave/btrfs-progs/blob/first/INSTALL#L4


Grab the source code from the release repo
```
git clone git://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git
```

Build and install
```
cd btrfs-progs
./autogen.sh
./configure --disable-documentation --disable-convert
make
```

```
sudo make install  # needs root access because it will install under /usr/local/bin and update /lib/udev/rules.d/64-btrfs-dm.rules
```


```
sudo btrfs --version  # should print "btrfs-progs v5.1" or greater
```
