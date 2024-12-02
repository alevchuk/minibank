# Go

We use Go for Lightning LND implementation and for monitoring services.


## Build Go

1. Fetch bootstrap go (as root)

```
sudo apt install -y golang git

```


--- after this commands should be run under the unix account where Go related services will be running. ---

for example login as Lighting user like this:
```
sudo su -l lightning
```


2. Set bootstrap path and gopath. Run:

```
echo 'export GOROOT_BOOTSTRAP="$(ls -1d /usr/lib/go-* | tail -n1)"' >> ~/.profile
echo 'export GOROOT=~/src/go' >> ~/.profile
echo 'export GOPATH=~/gocode' >> ~/.profile
echo 'export PATH=$GOROOT/bin:$GOPATH/bin:$PATH' >> ~/.profile
```

Load `~/.profile`
```
. ~/.profile
```

4. Fetch new go
```
git clone https://go.googlesource.com/go ~/src/go
cd ~/src/go
git fetch

git checkout $(git tag | grep go1.22.[0-9]*$ | sort -V | tail -n1) # checkout latest minor version

```
As of 2024-12 min version is 1.22, you can check it here https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md#installing-go

5. Build new go
```
. ~/.profile
cd $GOROOT/src
./make.bash
```
At the end it should say "Installed commands in $GOROOT/bin"
