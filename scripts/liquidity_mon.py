#!/usr/bin/env python3

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

PUBKEY_MAP = {
    "031015a": "breez1",
    "02247d9": "lnbig26"
}

LOCAL_BALANCE_GAUGE = Gauge(
    "local_balance_sats",
    "Amount of outbound liquidity (sats)",
    ["remote_node"]
)

REMOTE_BALANCE_GAUGE = Gauge(
    "remote_balance_sats",
    "Amount of inbound liquidity (sats)",
    ["remote_node"]
)

NETWORK_INFO_GAUGE = Gauge(
    "network_info",
    "Various metrics",
    ["metric"]
)

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


def active_channels_with_local_balances(channels):
  results = []
  for c in channels:
    if c["active"] == True:
      if int(c["local_balance"]) > 0 or True:
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
        channels_with_local = active_channels_with_local_balances(channels)
        channels_with_remote = active_channels_with_remote_balances(channels)
        
        for pubkey_prefix, local_name in PUBKEY_MAP.items():
            total_l = 0
            for c in channels_with_remote:
                if c["remote_pubkey"].startswith(pubkey_prefix):
                    total_l += int(c["local_balance"])
        
            logger.debug("Local {}: {}".format(local_name, total_l))
            LOCAL_BALANCE_GAUGE.labels(local_name).set(total_l)

            total_r = 0
            for c in channels_with_remote:
                if c["remote_pubkey"].startswith(pubkey_prefix):
                    total_r += int(c["remote_balance"])
        
            logger.debug("Remote {}: {}".format(local_name, total_r))
            REMOTE_BALANCE_GAUGE.labels(local_name).set(total_r)

        total_local_balance = sum(int(c['local_balance']) for c in channels_with_local)
        total_remote_balance = sum(int(c['remote_balance']) for c in channels_with_remote)

        logger.debug("total local: {}".format(total_local_balance))
        LOCAL_BALANCE_GAUGE.labels("total").set(total_local_balance)

        logger.debug("total remote: {}".format(total_remote_balance))
        REMOTE_BALANCE_GAUGE.labels("total").set(total_remote_balance)

        # Get Netwrok Info
        info = json.loads(subprocess.check_output(["lncli", "getnetworkinfo"]).decode("utf-8"))
        for metric, value in info.items():
            NETWORK_INFO_GAUGE.labels(metric).set(value)

        time.sleep(5)
    

if __name__ == "__main__":
    main()
