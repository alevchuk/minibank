# Grafana on Raspberry Pi 4

This manual documents how to build and run Grafana on Pi 4. The main challenge is that Grafana requires a 64-bit environment while Pi base operating system Rasbian is 32-bit. Funtualty Pi 4 hardware is 64-bit.

Grafana is a monitoring/analytics web interface.


Prereqisits:
 * [Node exporter running on all nodes](https://github.com/alevchuk/minibank/blob/master/README.md#prometheus-exporters) (calculates metrics locally)
 * [Prometheus running on one of the nodes](https://github.com/alevchuk/minibank/blob/master/README.md#prometheus) (aggragetes and stores all metrics in one place)


Citations:
* This section is based on the [officail grafana doc](https://github.com/grafana/grafana/blob/master/contribute/developer-guide.md#build-grafana)



## Chroot for 64-bit environment

```
sudo adduser --disabled-password grafana
sudo apt install -y debootstrap schroot

sudo apt install -y debootstrap schroot
cat << EOF | sudo tee /etc/schroot/chroot.d/pi64
[pi64]
description=builds that need 64-bit environment
type=directory
directory=/mnt/btrfs/pi64
users=grafana
root-groups=root
profile=desktop
personality=linux
preserve-environment=true
EOF

sudo debootstrap --arch arm64 /mnt/btrfs/pi64
sudo schroot -c pi64 -- apt install -y mesa-utils sudo


sudo mkdir /mnt/btrfs/pi64/mnt/btrfs/grafana
sudo mkdir /mnt/btrfs/pi64/mnt/btrfs/grafana/src
sudo mkdir /mnt/btrfs/pi64/mnt/btrfs/grafana/gocode
sudo mkdir /mnt/btrfs/pi64/mnt/btrfs/grafana/bin

sudo chown -R grafana /mnt/btrfs/pi64/mnt/btrfs/grafana
```

# Update firefall
```
sudo vi /etc/iptables/rules.v4
```
Add rule (modify -s if your subnet is different):
```
# Allow Grafana Web UI on local network
-A INPUT -p tcp -s 192.168.0.0/24 --dport 3000 -j ACCEPT
```
Reload firewall:
```
sudo systemctl restart netfilter-persistent.service
```

# Install needed packages
```
sudo schroot -c pi64 -- apt install -y python3.7 python3-distutils g++ make golang git
```


# Change user
Login as grafana user and drop into 64-bin environment:
```
sudo su -l grafana
schroot -c pi64

ln -s /mnt/btrfs/grafana/src ~/src
ln -s /mnt/btrfs/grafana/gocode ~/gocode
ln -s /mnt/btrfs/grafana/bin ~/bin
```

The remainging parts of this manual will assume you are logged into the 64-bin environment.


## Build Node.js 

Login as grafana user and drop into 64-bin environment:
```
sudo su -l grafana
schroot -c pi64
```

```
git clone https://github.com/nodejs/node.git ~/src/node
cd ~/src/node
git checkout $(git tag | grep v1 | sort -V | tail -n1)

cd ~/src/node && make clean && ./configure --prefix $HOME/bin && make && make install
```

## Build Go


1. Set bootstrap path and gopath. Add the following to `~/.profile`
to `~/.profile` add:
```
export GOROOT=~/src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH

export PATH=$HOME/bin/bin:$PATH

```

Load ~/.profile
```
. ~/.profile
```

4. Fetch new go
```
git clone https://go.googlesource.com/go ~/src/go
cd ~/src/go
git fetch
git checkout go1.13.1
```

5. Build new go
```
. ~/.profile
cd $GOROOT/src
./all.bash
```
At the end it should say "Installed commands in $GOROOT/bin"



# Download grafana

```
go get github.com/grafana/grafana
```


# Build Grafana front-end
```
cd $GOPATH/src/github.com/grafana/grafana

# IMPORTANT: before running `yarn install` you need to remove
#            "phantomjs-prebuilt" form ./github.com/grafana/grafana/package.json
#            more details on this here
#            https://github.com/grafana/grafana/issues/14115

yarn install --pure-lockfile
yarn start
```


# Build Grafana back-end
```
cd $GOPATH/src/github.com/grafana/grafana
make run
```

# Run
```
cd ~/gocode/src/github.com/grafana/grafana
./bin/linux-arm/grafana-server
```


# Use

Use grafana: connect your browser to http://localhost:3000

Follow web-ui wizard. Import dashboards node_exporter for Grafana app store.
E.g. "Node Exporter Server Metrics" can show multiple nodes side-by-side:


![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")
