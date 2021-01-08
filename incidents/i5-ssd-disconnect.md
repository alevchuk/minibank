SSD over USB 3 disconnected on Jan  6 05:59:45

Root-cause:
- This is most likely the issue with USB3.0 devices with bad UAS support https://www.raspberrypi.org/forums/viewtopic.php?t=245931
- ~~Along with UAS device firmare issues there was also a suggesting the USB 3.0 is interfering with 2.4 GHz Wi-Fi https://github.com/raspberrypi/linux/issues/3070)~~ 2.4 GHz Wi-Fi is not triggering issues (at least when UAS is disabled)

Mitigation:
- Disable UAS as per raspberrypi.org sticky forum post suggestion
- Also tired turning Off 2.4HZ Wi-Fi radio on the router (it's localed next to the Pi). When UAS is disabled there are no issues, regardless.


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



# Mitigation - turn off UAS

Device 1 - when plugged in to USB 2.0 port
```
[22028.692418] usb 1-1.4: new high-speed USB device number 5 using xhci_hcd
[22028.826859] usb 1-1.4: New USB device found, idVendor=0781, idProduct=558c, bcdDevice=10.12
[22028.826877] usb 1-1.4: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[22028.826889] usb 1-1.4: Product: Extreme SSD
[22028.826901] usb 1-1.4: Manufacturer: SanDisk
[22028.826912] usb 1-1.4: SerialNumber: 31393138314B343030363138
[22028.834938] scsi host2: uas
[22028.838078] scsi 2:0:0:0: Direct-Access     SanDisk  Extreme SSD      1012 PQ: 0 ANSI: 6
[22028.841011] sd 2:0:0:0: [sdc] Spinning up disk...
[22028.841440] sd 2:0:0:0: Attached scsi generic sg0 type 0
[22028.843834] scsi 2:0:0:1: Enclosure         SanDisk  SES Device       1012 PQ: 0 ANSI: 6
[22028.846788] scsi 2:0:0:1: Attached scsi generic sg1 type 13
[22029.856400] ..ready
[22030.882328] sd 2:0:0:0: [sdc] 976773120 512-byte logical blocks: (500 GB/466 GiB)
[22030.882336] sd 2:0:0:0: [sdc] 4096-byte physical blocks
[22030.882822] sd 2:0:0:0: [sdc] Write Protect is off
[22030.882829] sd 2:0:0:0: [sdc] Mode Sense: 67 00 10 08
[22030.883821] sd 2:0:0:0: [sdc] Write cache: disabled, read cache: enabled, supports DPO and FUA
[22030.884449] sd 2:0:0:0: [sdc] Optimal transfer size 33553920 bytes not a multiple of physical block size (4096 bytes)
[22030.939195] sd 2:0:0:0: [sdc] Write cache: enabled, read cache: enabled, supports DPO and FUA
[22030.939816] sd 2:0:0:0: [sdc] Attached SCSI disk
[22030.991181] BTRFS warning (device sdb): duplicate device /dev/sdc devid 1 generation 1142461 scanned by systemd-udevd (28346)
```

Device 1 - when plugged in to USB 3.0 port (Blue socket)
```
[22268.088868] usb 2-2: new SuperSpeed Gen 1 USB device number 2 using xhci_hcd
[22268.110067] usb 2-2: New USB device found, idVendor=0781, idProduct=558c, bcdDevice=10.12
[22268.110085] usb 2-2: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[22268.110097] usb 2-2: Product: Extreme SSD
[22268.110109] usb 2-2: Manufacturer: SanDisk
[22268.110120] usb 2-2: SerialNumber: 31393138314B343030363138
[22268.126553] scsi host2: uas
[22268.130296] scsi 2:0:0:0: Direct-Access     SanDisk  Extreme SSD      1012 PQ: 0 ANSI: 6
[22268.132051] sd 2:0:0:0: [sdc] Spinning up disk...
[22268.133074] sd 2:0:0:0: Attached scsi generic sg0 type 0
[22268.135407] scsi 2:0:0:1: Enclosure         SanDisk  SES Device       1012 PQ: 0 ANSI: 6
[22268.137369] scsi 2:0:0:1: Attached scsi generic sg1 type 13
[22269.156512] ..ready
[22270.182865] sd 2:0:0:0: [sdc] 976773120 512-byte logical blocks: (500 GB/466 GiB)
[22270.182882] sd 2:0:0:0: [sdc] 4096-byte physical blocks
[22270.183876] sd 2:0:0:0: [sdc] Write Protect is off
[22270.183894] sd 2:0:0:0: [sdc] Mode Sense: 67 00 10 08
[22270.184589] sd 2:0:0:0: [sdc] Write cache: disabled, read cache: enabled, supports DPO and FUA
[22270.185505] sd 2:0:0:0: [sdc] Optimal transfer size 33553920 bytes not a multiple of physical block size (4096 bytes)
[22270.231921] sd 2:0:0:0: [sdc] Write cache: enabled, read cache: enabled, supports DPO and FUA
[22270.233236] sd 2:0:0:0: [sdc] Attached SCSI disk
[22270.267633] BTRFS warning (device sdb): duplicate device /dev/sdc devid 1 generation 1142461 scanned by systemd-udevd (28382)
```


Device 2 - when plugged in to USB 2.0 port
```
[22090.285548] usb 1-1.3: new high-speed USB device number 6 using xhci_hcd
[22090.427653] usb 1-1.3: New USB device found, idVendor=04e8, idProduct=61f5, bcdDevice= 1.00
[22090.427670] usb 1-1.3: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[22090.427683] usb 1-1.3: Product: Portable SSD T5
[22090.427695] usb 1-1.3: Manufacturer: Samsung
[22090.427706] usb 1-1.3: SerialNumber: 1234567DAFFD
[22090.435160] scsi host3: uas
[22090.437111] scsi 3:0:0:0: Direct-Access     Samsung  Portable SSD T5  0    PQ: 0 ANSI: 6
[22090.439613] sd 3:0:0:0: Attached scsi generic sg2 type 0
[22090.441795] sd 3:0:0:0: [sdd] 976773168 512-byte logical blocks: (500 GB/466 GiB)
[22090.442409] sd 3:0:0:0: [sdd] Write Protect is off
[22090.442427] sd 3:0:0:0: [sdd] Mode Sense: 43 00 00 00
[22090.443291] sd 3:0:0:0: [sdd] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[22090.443986] sd 3:0:0:0: [sdd] Optimal transfer size 33553920 bytes
[22090.478678] sd 3:0:0:0: [sdd] Attached SCSI disk
[22090.561832] BTRFS warning (device sdb): duplicate device /dev/sdd devid 2 generation 1142461 scanned by systemd-udevd (28367)
```

Device 2 - when plugged in to USB 3.0 port (Blue socket)
```
[22341.090044] usb 2-1: new SuperSpeed Gen 1 USB device number 3 using xhci_hcd
[22341.118242] usb 2-1: New USB device found, idVendor=04e8, idProduct=61f5, bcdDevice= 1.00
[22341.118261] usb 2-1: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[22341.118273] usb 2-1: Product: Portable SSD T5
[22341.118284] usb 2-1: Manufacturer: Samsung
[22341.118296] usb 2-1: SerialNumber: 1234567DAFFD
[22341.136371] scsi host3: uas
[22341.139726] scsi 3:0:0:0: Direct-Access     Samsung  Portable SSD T5  0    PQ: 0 ANSI: 6
[22341.143092] sd 3:0:0:0: [sdd] 976773168 512-byte logical blocks: (500 GB/466 GiB)
[22341.143406] sd 3:0:0:0: [sdd] Write Protect is off
[22341.143420] sd 3:0:0:0: [sdd] Mode Sense: 43 00 00 00
[22341.144983] sd 3:0:0:0: [sdd] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[22341.145925] sd 3:0:0:0: Attached scsi generic sg2 type 0
[22341.147078] sd 3:0:0:0: [sdd] Optimal transfer size 33553920 bytes
[22341.174323] sd 3:0:0:0: [sdd] Attached SCSI disk
[22341.231316] BTRFS warning (device sdb): duplicate device /dev/sdd devid 2 generation 1142461 scanned by systemd-udevd (28393)
```

Editing boot command:
```
sudo vi /boot/cmdline.txt
```

So at the start of the line adding:
```
usb-storage.quirks=0781:558c:u,04e8:61f5:u
```
