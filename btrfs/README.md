# Get new features of BTRFS on Raspberry Pi


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
uname -a
```

## Step 2: Build and install btrfs-progs (userspace utilities)


Install dependencies
```
sudo apt-get install libuuid1 libblkid-dev liblzo2-dev zlibc libzstd-dev python-setuptools python3-setuptools
```
original list of dependencies is here https://github.com/kdave/btrfs-progs/blob/master/INSTALL#L4


Grab the source code from the release repo
```
git clone git://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git
```

Build and install
```
cd btrfs-progs
./autogen.sh
./configure --prefix /home/pi/bin --disable-documentation --disable-convert
make
make install
```

Add /home/pi/bin/bin to your PATH in ~/.profile
```
echo 'PATH="$HOME/bin/bin:$PATH"' >> ~/.profile
```
