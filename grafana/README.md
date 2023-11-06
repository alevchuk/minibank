# Grafana on Raspberry Pi 4

Grafana is a monitoring/analytics web interface.  This manual documents how to build and run Grafana on Pi 4.

Prerequisites:
 * [Node exporter running on all nodes](https://github.com/alevchuk/minibank/blob/first/README.md#prometheus-exporters) (calculates metrics locally)
 * [Prometheus running on one of the nodes](https://github.com/alevchuk/minibank/blob/first/README.md#prometheus) (aggregates and stores all metrics in one place)


Citations:
* This section is based on the [officail grafana doc](https://github.com/grafana/grafana/blob/first/contribute/developer-guide.md#build-grafana)



## Create directories

```
sudo adduser --disabled-password grafana
sudo mkdir /mnt/btrfs/grafana
sudo mkdir /mnt/btrfs/grafana/src
sudo mkdir /mnt/btrfs/grafana/gocode
sudo mkdir /mnt/btrfs/grafana/bin

sudo chown -R grafana /mnt/btrfs/grafana
```

# Setup firefall
https://github.com/alevchuk/minibank#network


# Install needed packages
```
sudo apt install -y python3 python3-distutils g++ make golang git
```

## Link to Go

1.  Enable Go. Add exports to ~/.profile by running:
```
sudo su -l grafana

ln -s /mnt/btrfs/grafana/src ~/src
ln -s /mnt/btrfs/grafana/gocode ~/gocode
ln -s /mnt/btrfs/grafana/bin ~/bin
ln -s /mnt/btrfs/lightning/src/ ~/src_readonly

echo 'export GOROOT=~/src_readonly/go' >> ~/.profile
echo 'export GOPATH=~/gocode' >> ~/.profile
echo 'export PATH=$GOROOT/bin:$GOPATH/bin:$PATH' >> ~/.profile
echo 'export PATH=$HOME/bin/bin:$PATH' >> ~/.profile
```

Load new profile
```
. ~/.profile
```


## Build Node.js 

Login as grafana user:
```
sudo su -l grafana
git clone https://github.com/nodejs/node.git ~/src/node
cd ~/src/node
git checkout $(git tag | grep v12 | sort -V | tail -n1)

cd ~/src/node && make clean && ./configure --prefix $HOME/bin && make && make install
```

# Install yarn
```
sudo su -l grafana
```

npm was installed as part of Node.js so you can just do this
```
npm install -g yarn
```

# Install grafana

```
sudo su -l grafana

git clone https://github.com/grafana/grafana.git ~/src/grafana
```


# Build Grafana front-end
```
cd ~/src/grafana

v=$(git tag | grep v9 | sort -V | tail -n1)
echo $v
git checkout $v

yarn install --pure-lockfile
yarn start
```


# Build Grafana back-end

```
cat /proc/sys/fs/inotify/max_user_watches # default is 8192 
sudo sysctl fs.inotify.max_user_watches=1048576 # increase to 1048576
```

```
sudo su -l grafana

cd ~/src/grafana
make run
```

# Run
```
cd ~/gocode/src/github.com/grafana/grafana
./bin/grafana-server
```

# Punch a hole in the firewall

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

Follow web-ui wizard. Import dashboards:
* Node Exporter Server Metrics dashboard https://gist.github.com/alevchuk/2a28d484945c86d3ffef0f7e671b065d
* Bitcoin dashboard https://gist.github.com/alevchuk/4235aefb3b8389b62c75878f5b1f7d04



E.g. "Node Exporter Server Metrics" can show multiple nodes side-by-side:

![alt text](https://raw.githubusercontent.com/alevchuk/minibank/first/img/grafana_screen_shot_2018-11-23.png "grafana monitoring dashboard using data from prometheus time-series store")

# Configure Hostnames
