#!/usr/bin/python3

import subprocess
import json
import sys
import logging
import time

from prometheus_client import Gauge, start_http_server

#
# A prometheus client to monitor LND inbound liquidity
#
# For documentation see
# https://github.com/alevchuk/minibank/blob/master/README.md#lnd-metrics
#

METRICS_PORT = 6549

REMOTE_BALANCE_GAUGE = Gauge(
    'remote_balance_sats',
    'Amount of inbound liquidity (sats)',
    ["node_name"]
)

PUBKEY_MAP = {
    "031015a": "breez1",
    "02247d9": "lnbig26"
}

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname).1s [%(filename)s:%(lineno)d] %(message)s')

    # Log to console (some)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = getLogger("liquidity_mon")

def active_channels_with_remote_balances(channels):
  results = []
  for c in channels:
    if c["active"] == True:
      if int(c["remote_balance"]) > 0 or True:
        results.append(c)

  if len(results) == 0:
      print("ERROR: no channels with remote balances, so there is nothing to balance")

  return results


def main():
    logger.info("Starting metrics on port {} ...".format(METRICS_PORT))
    start_http_server(METRICS_PORT)
    logger.info("Metrics server started")
    
    while True:
        channels = json.loads(subprocess.check_output(["lncli", "listchannels"]).decode("utf-8"))["channels"]
        channels_with_remote = active_channels_with_remote_balances(channels)
        
        for pubkey_prefix, local_name in PUBKEY_MAP.items():
            total = 0
            for c in channels_with_remote:
                if c["remote_pubkey"].startswith(pubkey_prefix):
                    total += int(c["remote_balance"])
        
            logger.debug("{}: {}".format(local_name, total))
            REMOTE_BALANCE_GAUGE.labels(local_name).set(total)
        
        total_remote_balance = sum(int(c['remote_balance']) for c in channels_with_remote)

        logger.debug("total: {}".format(total_remote_balance))
        REMOTE_BALANCE_GAUGE.labels("total").set(total_remote_balance)

        time.sleep(5)
    

if __name__ == "__main__":
    main()
