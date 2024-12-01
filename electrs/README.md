## Build Electrs


This manual documents how to build and run Electrs on Pi 4.

Prerequisites:
 * 64-bit OS and hardware
 * Login in as unix account that has sudo


# User
```
sudo adduser --disabled-password electrs  # hold Enter to answer all questions as default/yes
```

# Directories

Make directories inside the data mount point:
```
sudo mkdir /mnt/btrfs
sudo mkdir /mnt/btrfs/electrs
sudo mkdir /mnt/btrfs/electrs/src
sudo mkdir /mnt/btrfs/electrs/bin

sudo chown -R electrs /mnt/btrfs/electrs
```



# Install needed packages
```
sudo apt install -y git clang cmake build-essential curl
```


# Setup, git clone, and build

Login as electrs user:
```
sudo su -l electrs
```

Make symlinks back to data mount point
```
ln -s /mnt/btrfs/electrs/bin ~/bin
ln -s /mnt/btrfs/electrs/src ~/src

echo 'export PATH=$HOME/bin:$PATH  # electrs is here' >> ~/.bashrc
. ~/.bashrc
```

## Install rust
Login as electrs user and drop into 64-bin environment:
```
sudo su -l electrs
```

While logged in as electrs user:
```
cd src/
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rustup.sh
chmod +x rustup.sh
./rustup.sh

mv ~/.rustup ~/src/dot-rustup
ln -s ~/src/dot-rustup ~/.rustup

mv ~/.cargo ~/src/dot-cargo 
ln -s ~/src/dot-cargo ~/.cargo

. ~/.bashrc
```

## Build electrs

Login as electrs user:
```
sudo su -l electrs
```

While logged in as electrs schroot:
```
cd ~/src/
git clone https://github.com/romanz/electrs
cd electrs
cargo build --locked --release

cp target/release/electrs ~/bin/
```


# Configure

https://github.com/romanz/electrs/blob/master/doc/config.md

# Run it

```
~/bin/electrs --electrum-rpc-addr 127.0.0.1:50001
```
