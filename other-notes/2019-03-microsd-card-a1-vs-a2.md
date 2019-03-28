# MicroSD Cards A1 vs A2 comparison

A1 and A2 are SD card Application Performance Classes

I compared the performance of A1 and A2 256GB micro-sd cards:
 * A1 https://camelcamelcamel.com/SanDisk-256GB-MicroSDXC-Memory-Adapter/product/B0758NHWS8
 * A2 https://camelcamelcamel.com/SanDisk-256GB-Extreme-microSD-Adapter/product/B07FCR3316

According to official SanDisk docs https://www.sdcard.org/developers/overview/application/index.html the A2 version should have 4x more IOPS.

In my comparison A2 indeed performs better. I stated bitcoind on 2 identical clones of the blockchain running on 2 identical Pi Zero hardware, with the only difference being the SD Cards. I observed the following:
 1. Bitcoind catch-up was faster on A2
 2. There was 2-4x higher rate of bytes being read out of the system with A2 micro-sd cards
 
 ![alt text](https://raw.githubusercontent.com/alevchuk/minibank/master/other-notes/a1-vs-a2.png "Raid-1 of 256GB microSD cards running bitcoind, A1 to A2 card class comparison")
