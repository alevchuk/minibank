# Go

We use Go for Lightning LND implementation and for monitoring services.


## Build Go

1. Fetch bootstrap go (as root)

```
sudo apt-get install golang
sudo apt-get install git
```


--- after this all commands should be run under the unix account where Go related services will be running. ---

2. Set bootstrap path and gopath. To `~/.profile` add:

```
export GOROOT_BOOTSTRAP="$(ls -1d /usr/lib/go-* | tail -n1)"

export GOROOT=~/src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
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



## Don't Build Go (if you can avoid it)

If your lucky to have a Linux distro that has go-1.13.1 or higher packaged, then you don't need to build go, and just do:

1. Fetch go and git
```
sudo apt-get install golang-1.13
sudo apt-get install git
```

2. Set bootstrap path and gopath.

Change to a user:
```
# sudo su -l USERNAME_THAT_WILL_NEED_GO
# For example: sudo su -l lightning
```

To `~/.profile` add:
```
export GOROOT=/usr/lib/go-1.13
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
```


