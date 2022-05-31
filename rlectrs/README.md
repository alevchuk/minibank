## Build RelctRS


This manual documents how to build and run Electrs on Pi 4. We're going to run it in a 64-bit environment while Pi base operating system Rasbian is 32-bit. Fortunately Pi 4 hardware is 64-bit.

Prerequisites:
 * Boot Pi in [64-bit mode](https://medium.com/for-linux-users/how-to-make-your-raspberry-pi-4-faster-with-a-64-bit-kernel-77028c47d653) 
 * Login in as unix account that has sudo


## Chroot for 64-bit environment

```
sudo adduser --disabled-password electrs
sudo apt install -y debootstrap schroot

cat << EOF | sudo tee /etc/schroot/chroot.d/electrs64
[electrs64]
description=builds that need 64-bit environment
type=directory
directory=/mnt/btrfs/electrs64
users=electrs
root-groups=root
profile=desktop
personality=linux
preserve-environment=true
EOF

sudo debootstrap --arch arm64 buster /mnt/btrfs/electrs64

sudo schroot -c electrs64 -- apt update
sudo schroot -c electrs64 -- apt upgrade -y
```

Make directories inside the data mount point:
```
sudo mkdir /mnt/btrfs/electrs64/mnt/btrfs
sudo mkdir /mnt/btrfs/electrs64/mnt/btrfs/electrs
sudo mkdir /mnt/btrfs/electrs64/mnt/btrfs/electrs/src
sudo mkdir /mnt/btrfs/electrs64/mnt/btrfs/electrs/bin

sudo chown -R electrs /mnt/btrfs/electrs64/mnt/btrfs/electrs
```



# Install needed packages
```
sudo schroot -c electrs64 -- apt install -y git clang cmake build-essential 
```


# Setup, git clone, and build

Login as electrs user and drop into 64-bin environment:
```
sudo su -l electrs
schroot -c electrs64
```

Make symlinks back to data mount point
```
ln -s /mnt/btrfs/electrs/bin ~/bin
ln -s /mnt/btrfs/electrs/src ~/src

echo 'export PATH=$HOME/bin/bin:$PATH  # electrs is here' >> ~/.profile
. ~/.profile
```
