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


2. As of 2024-12 the min version for LND is go1.22, you can check it here https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md#installing-go so we will build go in multiple bootstrap cycles following the official compilers requierment https://go.dev/doc/install/source#go14

* go1.15 to 1.17
* go1.17 to go1.20
* go1.20 to 1.22


Set bootstrap path

```
export GOROOT_BOOTSTRAP="$(ls -1d /usr/lib/go-* | tail -n1)"
export GOROOT=~/src/go
export GOPATH=~/gocode
```

3. Fetch go1.17 source code
```
git clone https://go.googlesource.com/go ~/src/go
cd ~/src/go
git fetch

git checkout $(git tag | grep go1.17.[0-9]*$ | sort -V | tail -n1) # checkout latest minor version
```

5. Build
```
cd $GOROOT/src
./make.bash
```
At the end it should say "Installed commands in $GOROOT/bin"

6. Copy go to a tmp directory
```
mkdir -p ~/tmp/go1.17
cp -r $GOROOT/ ~/tmp/go1.17/
```

7. Set bootstrap path

```
export GOROOT_BOOTSTRAP="$HOME/tmp/go1.17"
export GOROOT=~/src/go
export GOPATH=~/gocode
```

8. Fetch go1.20 source code
```
cd ~/src/go
git fetch

git checkout $(git tag | grep go1.20.[0-9]*$ | sort -V | tail -n1) # checkout latest minor version
```

9. Build
```
cd $GOROOT/src
./make.bash
```
At the end it should say "Installed commands in $GOROOT/bin"

10. Copy go to a tmp directory
```
mkdir -p ~/tmp/go1.20
cp -r $GOROOT/ ~/tmp/go1.20/
```

11. Set bootstrap path

```
export GOROOT_BOOTSTRAP="$HOME/tmp/go1.20"
export GOROOT=~/src/go
export GOPATH=~/gocode
```

12. Fetch go1.23 source code
```
cd ~/src/go
git fetch

git checkout $(git tag | grep go1.23.[0-9]*$ | sort -V | tail -n1) # checkout latest minor version
```

13. Finally, build the modern go
```
cd $GOROOT/src
./make.bash
```
At the end it should say "Installed commands in $GOROOT/bin"
