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

## Configure

Edit /etc/tor/torrc
uncomment "ControlPort 9051"

TODO: figure out how to use HashedControlPassword

## Run Tor

```
/usr/local/bin/tor -f /etc/tor/torrc
```

## Config for systemd to run tor automatically

Add 3 files:
* /lib/systemd/system/tor@default.service
* /lib/systemd/system/tor.service
* /lib/systemd/system/tor@.service

**/lib/systemd/system/tor@default.service**
```
[Unit]
Description=Anonymizing overlay network for TCP
After=network.target nss-lookup.target
PartOf=tor.service
ReloadPropagatedFrom=tor.service

[Service]
Type=notify
NotifyAccess=all
PIDFile=/run/tor/tor.pid
PermissionsStartOnly=yes
ExecStartPre=/usr/local/bin/install -Z -m 02755 -o debian-tor -g debian-tor -d /run/tor
ExecStartPre=/usr/local/bin/tor --defaults-torrc /usr/local/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0 --verify-config
ExecStart=/usr/local/bin/tor --defaults-torrc /usr/local/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0
ExecReload=/bin/kill -HUP ${MAINPID}
KillSignal=SIGINT
TimeoutStartSec=300
TimeoutStopSec=60
Restart=on-failure
LimitNOFILE=65536

# Hardening
AppArmorProfile=-system_tor
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectHome=yes
ProtectSystem=full
ReadOnlyDirectories=/
ReadWriteDirectories=-/proc
ReadWriteDirectories=-/var/lib/tor
ReadWriteDirectories=-/var/log/tor
ReadWriteDirectories=-/run
CapabilityBoundingSet=CAP_SETUID CAP_SETGID CAP_NET_BIND_SERVICE CAP_DAC_READ_SEARCH
```

**/lib/systemd/system/tor.service**
```
# This service is actually a systemd target,
# but we are using a service since targets cannot be reloaded.

[Unit]
Description=Anonymizing overlay network for TCP (multi-instance-master)

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/true
ExecReload=/bin/true

[Install]
WantedBy=multi-user.target
```


**/lib/systemd/system/tor@.service**
```
[Unit]
Description=Anonymizing overlay network for TCP (instance %i)
After=network.target nss-lookup.target
PartOf=tor.service
ReloadPropagatedFrom=tor.service

[Service]
Type=notify
NotifyAccess=all
PIDFile=/run/tor-instances/%i/tor.pid
PermissionsStartOnly=yes
ExecStartPre=/usr/local/bin/install -Z -m 02755 -o _tor-%i -g _tor-%i -d /run/tor-instances/%i
ExecStartPre=/bin/sed -e 's/@@NAME@@/%i/g; w /run/tor-instances/%i.defaults' /usr/local/share/tor/tor-service-defaults-torrc-instances
ExecStartPre=/usr/local/bin/tor --defaults-torrc /run/tor-instances/%i.defaults -f /etc/tor/instances/%i/torrc --verify-config
ExecStart=/usr/local/bin/tor --defaults-torrc /run/tor-instances/%i.defaults -f /etc/tor/instances/%i/torrc
ExecReload=/bin/kill -HUP ${MAINPID}
KillSignal=SIGINT
TimeoutStartSec=300
TimeoutStopSec=60
Restart=on-failure
LimitNOFILE=65536

# Hardening
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectHome=yes
ProtectSystem=full
ReadOnlyDirectories=/
# We would really like to restrict the next item to [..]/%i but we can't,
# as systemd does not support that yet.  See also #781730.
ReadWriteDirectories=-/var/lib/tor-instances
ReadWriteDirectories=-/run
CapabilityBoundingSet=CAP_SETUID CAP_SETGID CAP_NET_BIND_SERVICE CAP_DAC_READ_SEARCH

[Install]
WantedBy=multi-user.target
```


## Enable Tor in LND
Run lnd with two extra arguments:
```
lnd --externalip=$(dig +short myip.opendns.com @resolver1.opendns.com):9735 --tor.active --tor.v3
```