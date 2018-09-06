# ltcd

# Prerequsits

LND and it's dependencies need to be fetched.

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
wget https://raw.githubusercontent.com/ltcsuite/ltcd/master/sample-ltcd.conf

diff sample-ltcd.conf ltcd.conf  # Check if you already have existing config
mv sample-ltcd.conf ltcd.conf  # Overwrite
```

# Testnet

In  `~/.ltcd/ltcd.conf` uncomment `testnet=1`
