SSD over USB 3 disconnected on Jan  6 05:59:45

Root-cause:
This is most likely the issue with USB3.0 devices with bad UAS support https://www.raspberrypi.org/forums/viewtopic.php?t=245931
https://github.com/raspberrypi/linux/issues/3070

Attempted mitigation:
- Going to try switching cables to UBS2 ports


syslog
```
Jan  6 04:09:47 bl5 rngd[360]: stats: entropy added to kernel pool: 4980000
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2 successes: 251
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2 failures: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Monobit: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Poker: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Runs: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Long run: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Continuous run: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: HRNG source speed: (min=224.696; avg=477.987; max=500.198)Kibits/s
Jan  6 04:09:47 bl5 rngd[360]: stats: FIPS tests speed: (min=3.746; avg=22.506; max=31.474)Mibits/s
Jan  6 04:09:47 bl5 rngd[360]: stats: Lowest ready-buffers level: 2
Jan  6 04:09:47 bl5 rngd[360]: stats: Entropy starvations: 0
Jan  6 04:09:47 bl5 rngd[360]: stats: Time spent starving for entropy: (min=0; avg=0.000; max=0)us
Jan  6 04:17:01 bl5 CRON[21529]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Jan  6 04:41:37 bl5 Tor[21309]: Tried for 120 seconds to get a connection to [scrubbed]:28870. Giving up. (waiting for circuit)
Jan  6 04:50:08 bl5 Tor[21309]: Heartbeat: Tor's uptime is 5 days 0:00 hours, with 15 circuits open. I've sent 45.89 MB and received 196.57 MB.
Jan  6 04:50:08 bl5 Tor[21309]: Average packaged cell fullness: 52.192%. TLS write overhead: 5%
Jan  6 05:09:47 bl5 rngd[360]: stats: bits received from HRNG source: 5060064
Jan  6 05:09:47 bl5 rngd[360]: stats: bits sent to kernel pool: 5010240
Jan  6 05:09:47 bl5 rngd[360]: stats: entropy added to kernel pool: 5010240
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2 successes: 253
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2 failures: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Monobit: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Poker: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Runs: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Long run: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS 140-2(2001-10-10) Continuous run: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: HRNG source speed: (min=224.696; avg=478.120; max=500.198)Kibits/s
Jan  6 05:09:47 bl5 rngd[360]: stats: FIPS tests speed: (min=3.746; avg=22.512; max=31.474)Mibits/s
Jan  6 05:09:47 bl5 rngd[360]: stats: Lowest ready-buffers level: 2
Jan  6 05:09:47 bl5 rngd[360]: stats: Entropy starvations: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: Time spent starving for entropy: (min=0; avg=0.000; max=0)us
Jan  6 05:17:01 bl5 CRON[32318]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Jan  6 05:53:52 bl5 systemd[1]: Started Session 212 of user pi.
Jan  6 05:59:45 bl5 kernel: [604209.906974] sd 1:0:0:0: [sdb] tag#4 uas_eh_abort_handler 0 uas-tag 5 inflight: CMD OUT
Jan  6 05:59:45 bl5 kernel: [604209.906984] sd 1:0:0:0: [sdb] tag#4 CDB: opcode=0x2a 2a 00 17 f7 19 a8 00 00 38 00
Jan  6 05:59:45 bl5 kernel: [604209.907334] sd 1:0:0:0: [sdb] tag#2 uas_eh_abort_handler 0 uas-tag 1 inflight: CMD OUT
Jan  6 05:59:45 bl5 kernel: [604209.907339] sd 1:0:0:0: [sdb] tag#2 CDB: opcode=0x2a 2a 00 17 f8 01 00 00 00 38 00
Jan  6 05:59:45 bl5 kernel: [604209.907429] sd 1:0:0:0: [sdb] tag#1 uas_eh_abort_handler 0 uas-tag 4 inflight: CMD OUT
Jan  6 05:59:45 bl5 kernel: [604209.907433] sd 1:0:0:0: [sdb] tag#1 CDB: opcode=0x2a 2a 00 17 f8 00 80 00 00 80 00
Jan  6 05:59:45 bl5 kernel: [604209.907543] sd 1:0:0:0: [sdb] tag#0 uas_eh_abort_handler 0 uas-tag 3 inflight: CMD
Jan  6 05:59:45 bl5 kernel: [604209.907548] sd 1:0:0:0: [sdb] tag#0 CDB: opcode=0x2a 2a 00 17 f8 00 58 00 00 28 00
Jan  6 05:59:45 bl5 kernel: [604209.943024] sd 1:0:0:0: [sdb] tag#28 uas_eh_abort_handler 0 uas-tag 13 inflight: CMD IN
Jan  6 05:59:45 bl5 kernel: [604209.943035] sd 1:0:0:0: [sdb] tag#28 CDB: opcode=0x28 28 00 28 36 5b f0 00 00 08 00
Jan  6 05:59:45 bl5 kernel: [604209.943306] sd 1:0:0:0: [sdb] tag#27 uas_eh_abort_handler 0 uas-tag 11 inflight: CMD IN
Jan  6 05:59:45 bl5 kernel: [604209.943311] sd 1:0:0:0: [sdb] tag#27 CDB: opcode=0x28 28 00 28 36 5b 58 00 00 08 00
Jan  6 05:59:45 bl5 kernel: [604209.943475] sd 1:0:0:0: [sdb] tag#26 uas_eh_abort_handler 0 uas-tag 10 inflight: CMD IN
Jan  6 05:59:45 bl5 kernel: [604209.943480] sd 1:0:0:0: [sdb] tag#26 CDB: opcode=0x28 28 00 28 36 5b 40 00 00 08 00
Jan  6 05:59:45 bl5 kernel: [604209.943601] sd 1:0:0:0: [sdb] tag#25 uas_eh_abort_handler 0 uas-tag 9 inflight: CMD IN
```


demon.log
```
Jan  6 05:09:47 bl5 rngd[360]: stats: Lowest ready-buffers level: 2
Jan  6 05:09:47 bl5 rngd[360]: stats: Entropy starvations: 0
Jan  6 05:09:47 bl5 rngd[360]: stats: Time spent starving for entropy: (min=0; avg=0.000; max=0)us
Jan  6 05:53:52 bl5 systemd[1]: Started Session 212 of user pi.
Jan  6 06:01:32 bl5 systemd[1]: Unmounting /mnt/btrfs...
Jan  6 06:01:32 bl5 umount[7914]: umount: /mnt/btrfs: target is busy.
Jan  6 06:01:32 bl5 systemd[1]: mnt-btrfs.mount: Mount process exited, code=exited, status=32/n/a
Jan  6 06:01:32 bl5 systemd[1]: Failed unmounting /mnt/btrfs.
Jan  6 06:01:32 bl5 systemd[1]: mnt-btrfs.mount: Unit is bound to inactive unit dev-sdb.device. Stopping, too.
Jan  6 06:01:32 bl5 systemd[1]: Unmounting /mnt/btrfs...
Jan  6 06:01:32 bl5 umount[7915]: umount: /mnt/btrfs: target is busy.
Jan  6 06:01:32 bl5 systemd[1]: mnt-btrfs.mount: Mount process exited, code=exited, status=32/n/a
Jan  6 06:01:32 bl5 systemd[1]: Failed unmounting /mnt/btrfs.
Jan  6 06:01:32 bl5 systemd[1]: mnt-btrfs.mount: Unit is bound to inactive unit dev-sdb.device. Stopping, too.
Jan  6 06:01:32 bl5 systemd[1]: Unmounting /mnt/btrfs...
```

