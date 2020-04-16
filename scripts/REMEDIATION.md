# Remediation

The following is implemented in a python script as a single file with no dependencies: https://github.com/alevchuk/minibank/blob/master/scripts/remediation.py

## Issues and Cause

CPU at 100%. In this state, LND times out when trying to generate or list invoices over RPC. See issue https://github.com/lightningnetwork/lnd/issues/3370 open since Aug 2019. LND `go` seems to be stuck in GC / Malloc for the ZMQ.


## Detection

At healthy state hosts of sizes roughly equivalent to AWS t2.small (1 cpu, 2gb ram) to t2.medium (2 cpu, 4gb ram) running BTCD and LND will not exceed 30% of CPU utilization for prolonged periods of time.

To find the time when the remediation is necessary do the following:
1. Read out the CPU utilization from /proc/stat
2. Sum up the relevant types of CPU use `user + nice + system  + steal`
3. Attempt to measure this every 15 seconds
4. Check if this metrics exceeds 0.3 in more than 50% of measurments within a 4 minute window


## Remediation

Find the PID of LND and issue a kill 15. If the process is still alive after 30 seconds issue a kill 9.

LND launcher needs to be setup so that it restarts itself automatically. Auto-unlock also needs to be in place.


## Setup

### Run LND so that it restarts automatically

```
while :; do lnd; sleep 5; done
```

### Auto Unlocker


### Run remediation script continuously



