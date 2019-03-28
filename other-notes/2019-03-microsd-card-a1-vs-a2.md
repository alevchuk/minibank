# MicroSD Cards A1 vs A2

I compared the performanc of A1 and A2 256GB cards:
 * A1 https://camelcamelcamel.com/SanDisk-256GB-MicroSDXC-Memory-Adapter/product/B0758NHWS8
 * A2 https://camelcamelcamel.com/SanDisk-256GB-Extreme-microSD-Adapter/product/B07FCR3316

According to official SanDisk docs https://www.sdcard.org/developers/overview/application/index.html the A2 version should have 4x more IOPS.

In my comparison A2 indeed performs better. I stated bitcoind on 2 identical clones of the blockchain running on 2 identical Pi Zero hardware, with the only difference being the SD Cards. I observed the following:
 1. Bitcoind catchup was faster on A2
 2. There was 2-4x more bytes read out of the A2 system
 
 
