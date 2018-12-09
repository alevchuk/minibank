= Go =

We use Go for Lightning LND implementation and for monitoring services.


== Build Go ==

1. Fetch bootstrap go (as root)

```
sudo apt-get install golang-1.6
sudo apt-get install git
```


--- after this all commands should be run under the unix account where Go related services will be running. ---

2. Set bootstrap path and gopath. To ~/.profile add:

```
export GOROOT_BOOTSTRAP=/usr/lib/go-1.6

export GOROOT=~/src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
```

4. Fetch new go
```
git clone https://go.googlesource.com/go ~/src/go
cd go
git fetch
git checkout go1.11.2
```

5. Build new go
```
. ~/.profile
cd $GOROOT/src
./all.bash
```
At the end it should say "Installed commands in $GOROOT/bin"
