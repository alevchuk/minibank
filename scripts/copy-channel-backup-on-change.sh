#!/bin/bash

# Setup: sudo mkdir -p /opt/local-backups/backups
# Copy systemd config from https://gist.github.com/alexbosworth/2c5e185aedbdac45a03655b709e255a3

SRC="/mnt/btrfs/lightning64/mnt/btrfs/lightning/lnd-data/data/chain/bitcoin/mainnet/channel.backup"
DST="/opt/local-backups/backups/channel.backup"

while true; do
    inotifywait $SRC
    final_dst="$DST.$(date +"%Y-%m-%d--%H%M%S")"

    rm -f $DST.latest
    ln -s "$final_dst" "$DST.latest"

    cp "$SRC" "$final_dst"
done
