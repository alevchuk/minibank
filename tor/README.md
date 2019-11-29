# Tor

## Build from source

Install dependencies: `apt-get install libevent-dev zlib1g-dev`

### Download source:
```
mkdir src
cd src

git clone https://git.torproject.org/tor.git
git checkout tor-0.4.1.6
```

### Verify:
```
git log -n1 | grep -A4 d10abc0929f4941d564b72a349aaf421aaa268f3
```

This should show you:

```
commit d10abc0929f4941d564b72a349aaf421aaa268f3
Author: Nick Mathewson <nickm@torproject.org>
Date:   Thu Sep 19 08:08:39 2019 -0400

    Set the date for the 0.4.1.6 release.
```


### Build and install:
```
sh autogen.sh && ./configure --disable-asciidoc && make
```

### Install
```
sudo make install
```
