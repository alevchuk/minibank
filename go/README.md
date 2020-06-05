# Go

We use Go for Lightning LND implementation and for monitoring services.


## Build Go

1. Fetch bootstrap go (as root)

```
sudo apt install golang git
```


--- after this commands should be run under the unix account where Go related services will be running. ---

2. Set bootstrap path and gopath. Add the following to `~/.profile`

```
export GOROOT_BOOTSTRAP="$(ls -1d /usr/lib/go-* | tail -n1)"

export GOROOT=~/src/go
export GOPATH=~/gocode
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
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
git checkout go1.13.1
```

5. (for 1 GB RAM hosts only) Add swap

If you have 1 GB of RAM or less then add another 1 GB of swap so that the build can finish.


"Log-out" (e.g. Ctrl-d) back to admin account.
```
sudo fallocate -l 2G /tmp/swapfile  # note, in some cases 1G may also be enough
sudo chmod 600 /tmp/swapfile
sudo mkswap /tmp/swapfile
sudo swapon /tmp/swapfile
```

Now log back into the user account where Go related services will be running.


6. Build new go
```
. ~/.profile
cd $GOROOT/src
./all.bash
```
At the end it should say "Installed commands in $GOROOT/bin"



## Don't Build Go (if you can avoid it)


If you have a Linux distro that has go-1.13.1 or higher packaged, then you don't need to build go, and just do:


* AWS Debian 10 (buster) image has this
* When Upgrading from Debian 9, you will not have this and will need to build

1. Fetch go and git
```
sudo apt install golang-1.13 git
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


