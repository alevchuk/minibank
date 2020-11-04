# LND iowait 100%

https://github.com/lightningnetwork/lnd/issues/4689

## Root-cause

Elevated gossip chatter was causing many `channelUpdate` events. It appears that channelUpdates are flushed to disk is a way that amount I/O is proportional to the amount of `channelUpdate` events.

## Prevention

Looks like the team is focusing a a prevent for this by filtering out gossip chatter that is not interesting to nodes. "Zombie channels" with no heartbeat yet generating a lot of `channelUpdate` events gossip are suspected.

I think this may not be the most effective prevention for this incident for reasons which I'll explain in the next section "O(1) vs O(N) I/O", yet the of course team is free to prioritize as they see fit. I admint that there are probably additional objectives and constraints that are not obvious from the outside.


## O(1) vs O(N) I/O

[Memory access in 50x to 500x faster than SSD disk access](https://www.quora.com/Is-the-speed-of-SSD-and-RAM-the-same/answer/Gediz-Gursu). Even without filtering gossip keeping the network topology of channels updates in memory only would not cause a this incident. The issue arises when network topology updates are persisted from memory to disk.

I propose that by tracking which channels need an update and periodically flushing out only those channels we would limit the I/O activit to 1 update for a given time period. Compare that to the current behaviour of persisting N updates in a given time window. The `channelUpate` behaviour from what I meansured [overwrites existing disk data](https://github.com/lightningnetwork/lnd/issues/4689#issuecomment-710028091) .This would of course make the disk data a little stale, so if LND crashes, after restart it may have a slightly outdated view of the network then it had in memory previously. This should not be a problem because outdated views of the network is already the nature of the gossip protocol. Morover, the time interval for flush to disk would constraint how satale the data can get.

Give that this solution effectively shifts performance bottelnecks from disk access to memory, we can expect a 50x to 500x improvement in I/O usage. Gossip filtering would need to reliability filter out 98% to 99.8% of messages to compete with this solution.

