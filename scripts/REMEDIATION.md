# Remediation

The following is implemented in a python script as a single file with no dependencies: https://github.com/alevchuk/minibank/blob/master/scripts/remediation.py

Table of contents
=================

  * [Issues and Cause](#issue-and-cause)
  * [Detection](#detection)
  * [Remediation](#remediation)
  * [Setup](#setup)
    * [Run LND so that it restarts automatically](#run-lnd-so-that-it-restarts-automatically)
    * [Auto Unlocker via cron](#auto-unlocker-via-cron)
    * [Run remediation](#run-remediation)
  
## Issue and Cause

CPU at 100%. In this state, LND times out when trying to generate or list invoices over RPC. See issue https://github.com/lightningnetwork/lnd/issues/3370 open since Aug 2019. LND `go` seems to be stuck in GC / Malloc for the ZMQ.


## Detection

At healthy state hosts of sizes roughly equivalent to AWS t2.small (1 cpu, 2gb ram) to t2.medium (2 cpu, 4gb ram) running BTCD and LND will not exceed 30% of CPU utilization for prolonged periods of time.

To find the time when the remediation is necessary do the following:
1. Read out the CPU utilization from /proc/stat
2. Sum up the relevant types of CPU use `user + nice + system  + steal`
3. Attempt to measure this every 15 seconds
4. Check if this metrics exceeds 0.3 in more than 50% of measurements within a 4 minute window


## Remediation

Find the PID of LND and issue a kill 15. If the process is still alive after 1 minute issue a kill 9.

LND launcher needs to be set up so that it restarts itself automatically. Auto-unlock also needs to be in place.


## Setup

### Run LND so that it restarts automatically

```
while :; do lnd; sleep 5; done
```

### Auto Unlocker via cron

For additional security create a separate user account for the unlocker. The password will be stored in a plain text file with only the unlocker and root having read access.

```
sudo /usr/sbin/adduser unlocker

sudo su -l unlocker

cat <<EOF > ./unlock
#!/bin/sh

cat /etc/secret/lnd_password | ~lightning/gocode/bin/lncli --tlscertpath=/home/lightning/.lnd/tls.cert unlock --stdin
EOF

chmod +x ./unlock

logout
```

Put the password on disk:
```
sudo mkdir /etc/secret
sudo touch /etc/secret/lnd_password
sudo chown unlocker /etc/secret/lnd_password
sudo chgrp root /etc/secret/lnd_password
sudo chmod u=rw,g=,o= /etc/secret/lnd_password

ls -l /etc/secret/lnd_password

sudo su -l unlocker

cat >> /etc/secret/lnd_password
```

After entering the password, press `Ctrl-d` and run `logout`

Run unlocker every minute:
```
sudo su -l unlocker
crontab -e
'''

### Text-editor will open, paste the following, save, and exit:


# m h  dom mon dow   command
* *    *   *   *     $HOME/unlock

'''
```

### Run remediation

Under the account that runs LND

Download the remediation script:
```
curl https://raw.githubusercontent.com/alevchuk/minibank/master/scripts/remediation.py > ./remediation.py
```

Inspect it:
```
vim ./remediation.py
```

Make it runnable:
```
chmod +x ./remediation.py
```

Run it:
```
./remediation.py
```
