# ltcd

# Update: 2019-09-06

Cancelling my LTC attempt... See [README.md](README.md)

# Archive before 2019-09-06

# Prerequsits

LND and it's dependencies need to be fetched. See https://github.com/alevchuk/pstm/blob/first/lnd-e2e-testing/README.md#get-lnd--btcd

# Build and Install

```
cd $GOPATH/src/github.com/ltcsuite/ltcd
git pull && glide install
go install . ./cmd/...
```

# Config

```

mkdir ~/.ltcd
cd ~/.ltcd/
wget https://raw.githubusercontent.com/ltcsuite/ltcd/first/sample-ltcd.conf

diff sample-ltcd.conf ltcd.conf  # Check if you already have existing config
mv sample-ltcd.conf ltcd.conf  # Overwrite
```

Edit **~/.ltcd/ltcd.conf**

Type a bunch of random alphanumberic characters for RPC user and password:
```
rpcuser=
rpcpass=
```

# Testnet

In  `~/.ltcd/ltcd.conf` uncomment `testnet=1`
