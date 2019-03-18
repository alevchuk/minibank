#!/usr/bin/python3

import subprocess
import random
import time
import json
import sys

def r(cmd):
    return subprocess.check_output(cmd).decode('utf-8').strip()

def ts():
    return r(['date', '+%Y-%m-%dT%H:%M:%S%z'])  # shows local timiezone

print(ts())
channels = json.loads(r(['lncli', 'listchannels']))['channels']
print('Total channels: {}'.format(len(channels)))

if '--4real' in sys.argv:
    FOR_REAL = True
    LOG_PREFIX = ''
else:
    FOR_REAL = False  # default is try run
    LOG_PREFIX = 'DRY '


random.shuffle(channels)
for c in channels:
    cp = c['channel_point']
    rpk = c['remote_pubkey']
    funding_txn, output_index = cp.split(':', 1)

    keep = False
    # This is the "custom" part, modify as needed
    for good_pubkey in ['02d58', '039ed', '03fb8', '030995', '033e9', '02275']:
        if good_pubkey in rpk:
            keep = True

    if keep:
        continue  # don't close this channel

    print('{}Closing {} index={} remote_pubkey={}'.format(LOG_PREFIX, funding_txn, output_index, rpk))

    close_cmd = ['lncli', 'closechannel', funding_txn, '--output_index', output_index]
    print('  {}'.format(' '.join(close_cmd)))

    if FOR_REAL:
        try:
            out = r(close_cmd)
            print(json.loads(out.decode('utf-8')))
        except Exception as e:
            print(e)
            print("Graceful attempt failed, force closing the channel!")
            print("Sleeping for 10 seconds before force closing...")
            time.sleep(10)
            print('Force closing {} index={} remote_pubkey={}'.format(funding_txn, output_index, rpk))

            out = r(close_cmd + ['--force'])
            print(json.loads(out))

            print(ts())
            print("-------------------------------------")
