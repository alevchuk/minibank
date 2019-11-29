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

#### Step 1 of 2:
```
git log -n1 | grep -A4 d10abc0929f4941d564b72a349aaf421aaa268f3
```

This should show:

> `commit d10abc0929f4941d564b72a349aaf421aaa268f3` <br />
> `Author: Nick Mathewson <nickm@torproject.org>` <br />
> `Date:   Thu Sep 19 08:08:39 2019 -0400`<br />
> <br />
> `   Set the date for the 0.4.1.6 release.`


#### Step 2 of 2:
```
git status
```

This should show:

> `HEAD detached at tor-0.4.1.6` <br />
> `nothing to commit, working tree clean`

### Build and install:
```
sh autogen.sh && ./configure --disable-asciidoc && make
```

### Install
```
sudo make install
```
