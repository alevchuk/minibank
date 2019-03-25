#!/usr/bin/python3

import subprocess
import json
import sys

if len(sys.argv) > 1 and '--testnet' in sys.argv:
  net = ['--network=testnet']
else:
  net = []

date = subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S%z"]).decode("utf-8").strip()  # shows local Timezone
wallet_balance = json.loads(subprocess.check_output(["lncli", "walletbalance"]).decode("utf-8"))
channel_balance = json.loads(subprocess.check_output(["lncli", "channelbalance"]).decode("utf-8"))
pendingchannels = json.loads(subprocess.check_output(["lncli", "pendingchannels"]).decode("utf-8"))
chain_txns = json.loads(subprocess.check_output(["lncli", "listchaintxns"]).decode("utf-8"))["transactions"]
channels = json.loads(subprocess.check_output(["lncli", "listchannels"]).decode("utf-8"))["channels"]

wallet = int(wallet_balance["confirmed_balance"])
wallet_unconfirmed = int(wallet_balance["unconfirmed_balance"])

limbo_balance = int(pendingchannels['total_limbo_balance'])  # The balance in satoshis encumbered in pending channels
channel = int(channel_balance["balance"])
chain_fees = sum([int(i["total_fees"]) for i in chain_txns])

# Fees, to be paid for commitment transactions
commit_fees = sum([int(i["commit_fee"]) for i in channels])
commit_fees += sum([int(i["commit_fee"]) for i in (
  pendingchannels["pending_open_channels"] +
  pendingchannels["pending_closing_channels"] +
  pendingchannels["pending_force_closing_channels"] +
  pendingchannels["waiting_close_channels"])
if "commit_fee" in i])

# All fees
fees = chain_fees + commit_fees  # TODO: add Lightning relay fees

pending_htlcs = 0
for ch in channels:
  for htlc in ch.get("pending_htlcs", []):
    pending_htlcs += int(htlc["amount"])

pending = int(channel_balance["pending_open_balance"]) + limbo_balance + pending_htlcs + wallet_unconfirmed
balance = wallet + channel + pending

if len(sys.argv) < 2 or sys.argv[1] != '--no-header':
    print(
      "Time\t\t\t"

      "Wallet\t\t"
      "Pending\t\t"
      "Channel\t\t"
      "Fees\t\t"
      "Balance\t\t"
      "Balance+Fees"
    )

print(
  date + \
  "\t{:,}".format(wallet + wallet_unconfirmed) + \
  "\t{:,}".format(pending) + \
  "\t{:,}".format(channel) + \
  "\t{:,}".format(fees) + \
  "\t{:,}".format(balance) + \
  "\t{:,}".format(balance + fees)
)

# Setup:
'''
chmod +x ~/lnd-e2e-testing/get_balance_report.py
~/lnd-e2e-testing/get_balance_report.py > ~/balance_history.tab
crontab -e
'''
## Text-editor will open, paste the following, save, and exit:
'''
SHELL=/bin/bash
# m h  dom mon dow   command
0   *  *   *   *     (source ~/.profile; ~/lnd-e2e-testing/get_balance_report.py --no-header >> ~/balance_history.tab) 2> /tmp/stderr_cron_get_balance_report
'''

# Check balance:
'''
while :; do (cat ~/balance_history.tab; ~/lnd-e2e-testing/get_balance_report.py) | column -t; sleep 60; done
'''
# Example Output:
# Time                       Wallet       Pending      Channel      Fees         Balance      Balance+Fees
# 2018-07-15T13:00:01-07:00  1,599,749    208,344,076  150,652,120  248,117      360,595,945  360,844,062
# 2018-00-15T19:00:01-0700   18,113,811   208,312,757  134,928,908  248,117      361,355,476  361,603,593
# 2018-00-15T20:00:01-0700   18,113,811   208,312,757  134,611,917  248,117      361,038,485  361,286,602
# 2018-26-15T20:26:36-0700   18,113,811   208,312,757  134,007,409  248,117      360,433,977  360,682,094
