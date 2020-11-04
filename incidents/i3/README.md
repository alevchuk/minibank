# LND iowait 100%

https://github.com/lightningnetwork/lnd/issues/4689

## Root-cause

Elevated gossip chatter was causing many `channelUpdate` events. It appears that channelUpdates are flushed to disk is a way that amount I/O is proportional to the amount of `channelUpdate` events.

## Prevention

Looks like the team is focusing to prevent this by filtering out gossip chatter that is not interesting to nodes. "Zombie channels" with no heartbeat yet a lot of gossip are suspected to generate extra `channelUpdate` events.

I think this may not be the most effective prevention for this incident for reasons which I'll explain in the next section "O(1) vs O(N) I/O", yet the team may prioritize as they see fit because there may be additional objectives and constraints that are not obvious from the outside.


## O(1) vs O(N) I/O

Memory access in 30x faster than SSD disk access. Even without filtering I feel persisting the network topology of channels in memory will not cause a this incident. The issue arises when network topology updates are persisted from memory to disk. The updates overwrite existing disk data so persisting N updates in a given time window can be replaced with 1 update. This would of course make the disk data a little stale, so if LND crashes, after restart it may have a slightly outdated view of the network then it had in memory previously. This should not be a problem because outdated views of the network is already the nature of the gossip protocol. Mover, the time interval for flush to disk would constraint how satale the data can get.

