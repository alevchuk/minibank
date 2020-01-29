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

sudo mkdir /mnt/btrfs/grafana
sudo mkdir /mnt/btrfs/grafana/src
sudo mkdir /mnt/btrfs/grafana/gocode
sudo mkdir /mnt/btrfs/grafana/bin

sudo chown -R grafana /mnt/btrfs/grafana

sudo su -l grafana
ln -s /mnt/btrfs/lightning/src ~/lightning_src # symlink to read-only go installation
ln -s /mnt/btrfs/prometheus/bin ~/prometheus_bin # symlink to read-only node.js installation
ln -s /mnt/btrfs/grafana/src ~/src
ln -s /mnt/btrfs/grafana/gocode ~/gocode
ln -s /mnt/btrfs/grafana/bin ~/bin
```

```
sudo schroot -c pi64 -- apt install -y python3.7 python3-distutils g++ make golang git
```


## Build Node.js 


```
git clone https://github.com/nodejs/node.git ~/src/node
cd ~/src/node
git checkout $(git tag | grep v1 | sort -V | tail -n1)
./configure --prefix $HOME/bin
make clean && make && make install
```

## Build Go


to `~/.profile` add:
```
export GOROOT=~/lightning_src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$HOME/bin/bin:$PATH

export PATH=$HOME/prometheus_bin/bin:$PATH
export PATH=$HOME/lightning_src/go/bin:$PATH

```


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

# Use

Use grafana: connect your browser to http://localhost:3000

Follow web-ui wizard. Import dashboards node_exporter for Grafana app store.
E.g. "Node Exporter Server Metrics" can show multiple nodes side-by-side:


![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")
