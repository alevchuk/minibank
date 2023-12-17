# i6 - btrfs hanging

Dec 17, 2024
```
[422781.765939] usb 2-2: reset SuperSpeed USB device number 3 using xhci_hcd
[422916.774698] INFO: task kcompactd0:42 blocked for more than 120 seconds.
[422916.774722]       Tainted: G         C         6.1.21-v8+ #1642
[422916.774728] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[422916.774734] task:kcompactd0      state:D stack:0     pid:42    ppid:2      flags:0x00000008
[422916.774748] Call trace:
[422916.774753]  __switch_to+0xf8/0x1e0
[422916.774773]  __schedule+0x2a8/0x830
[422916.774782]  schedule+0x60/0x100
[422916.774791]  io_schedule+0x24/0x60
[422916.774800]  __folio_lock+0x128/0x218
[422916.774810]  migrate_pages+0x368/0xb78
[422916.774819]  compact_zone+0x6a0/0xe28
[422916.774825]  proactive_compact_node+0x94/0xc8
[422916.774832]  kcompactd+0x124/0x318
[422916.774838]  kthread+0xfc/0x110
[422916.774846]  ret_from_fork+0x10/0x20
[422916.774889] INFO: task btrfs-transacti:570 blocked for more than 120 seconds.
[422916.774896]       Tainted: G         C         6.1.21-v8+ #1642
[422916.774901] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[422916.774906] task:btrfs-transacti state:D stack:0     pid:570   ppid:2      flags:0x00000008
[422916.774917] Call trace:
[422916.774922]  __switch_to+0xf8/0x1e0
[422916.774931]  __schedule+0x2a8/0x830
[422916.774940]  schedule+0x60/0x100
[422916.774949]  io_schedule+0x24/0x60
[422916.774957]  blk_mq_get_tag+0x1ac/0x328
[422916.774968]  __blk_mq_alloc_requests+0x198/0x308
[422916.774976]  blk_mq_submit_bio+0x368/0x580
[422916.774984]  __submit_bio+0x1b0/0x2d0
[422916.774992]  submit_bio_noacct_nocheck+0x2d0/0x310
[422916.775000]  submit_bio_noacct+0x120/0x3a8
[422916.775007]  submit_bio+0x3c/0xf0
[422916.775015]  btrfs_submit_dev_bio+0xb8/0x148 [btrfs]
[422916.775136]  btrfs_submit_bio+0x27c/0x2a8 [btrfs]
[422916.775222]  btrfs_submit_metadata_bio+0x6c/0x100 [btrfs]
[422916.775307]  submit_one_bio+0x9c/0xd8 [btrfs]
[422916.775391]  read_extent_buffer_pages+0x240/0x700 [btrfs]
[422916.775475]  btrfs_read_extent_buffer+0x70/0x148 [btrfs]
[422916.775558]  read_tree_block+0x70/0xc0 [btrfs]
[422916.775641]  read_block_for_search+0x218/0x318 [btrfs]
[422916.775724]  btrfs_search_slot+0x300/0xa90 [btrfs]
[422916.775807]  lookup_inline_extent_backref+0x174/0x5f8 [btrfs]
[422916.775890]  __btrfs_free_extent.isra.65+0xec/0x11a0 [btrfs]
[422916.775972]  __btrfs_run_delayed_refs+0x250/0xf80 [btrfs]
[422916.776055]  btrfs_run_delayed_refs+0x74/0x288 [btrfs]
[422916.776137]  btrfs_commit_transaction+0x74/0xee8 [btrfs]
[422916.776220]  transaction_kthread+0x198/0x1d8 [btrfs]
[422916.776302]  kthread+0xfc/0x110
[422916.776310]  ret_from_fork+0x10/0x20
```

Did: `sudo reboot` host did not come back right away but eventually did. In 30 minutes I check by running `ssh`  and get in, `dmesg` is:

```
[   10.870088] Btrfs loaded, crc32c=crc32c-generic, zoned=no, fsverity=no
[   10.879567] BTRFS: device label minibank4 devid 4 transid 3292839 /dev/sda scanned by systemd-udevd (196)
[   10.887566] BTRFS: device label minibank4 devid 3 transid 3292839 /dev/sdb scanned by systemd-udevd (210)
[   11.313771] BTRFS info (device sdb): using crc32c (crc32c-generic) checksum algorithm
[   11.313842] BTRFS info (device sdb): disk space caching is enabled
[   11.501063] bcmgenet fd580000.ethernet: configuring instance for external RGMII (RX delay)
[   11.502942] bcmgenet fd580000.ethernet eth0: Link is Down
[   11.939697] BTRFS info (device sdb): start tree-log replay
[   13.028106] BTRFS info (device sdb): the free space cache file (6422575185920) is invalid, skip it
[   13.405551] BTRFS warning (device sdb): block group 6380699254784 has wrong amount of free space
[   13.405577] BTRFS warning (device sdb): failed to load free space cache for block group 6380699254784, rebuildin
g it now
[   15.118745] BTRFS info (device sdb): checking UUID tree
[   15.588241] bcmgenet fd580000.ethernet eth0: Link is Up - 1Gbps/Full - flow control rx/tx
[   15.588284] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready
```

No btrfs error recorded:
```
sudo btrfs dev stats -z /mnt/btrfs/
[/dev/sdb].write_io_errs    0
[/dev/sdb].read_io_errs     0
[/dev/sdb].flush_io_errs    0
[/dev/sdb].corruption_errs  0
[/dev/sdb].generation_errs  0
[/dev/sda].write_io_errs    0
[/dev/sda].read_io_errs     0
[/dev/sda].flush_io_errs    0
[/dev/sda].corruption_errs  0
[/dev/sda].generation_errs  0
```
