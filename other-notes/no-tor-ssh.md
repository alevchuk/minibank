SSH over Tor is very slow

Yet Tor provides more privacy

If you still want to SSH over the without Tor (e.g. only over local network) you can do this:



19. Write down your IP adress. To look it up run `sudo ifconfig`
20. Allow SSH in the firewall `sudo vi /etc/iptables/rules.v4` then add "Allow SSH" line so it's like this:
```
*filter
:INPUT DROP [152:211958]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [52247:3125304]
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT

# <-------- Allow SSH from home network only !
-A INPUT -p tcp -s 192.168.0.0/16  --dport 22 -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

COMMIT
``` 
* Leave IPv6 rules as the inital "Drop-everything" setup because most home networks do not need IPv6.

21. Run 
```
sudo /etc/init.d/netfilter-persistent restart
```

22. Run
```
sudo raspi-config
```
Select Interface Option -> SSH -> Yes

23. From your laptop, use the IP from step 5 and run: `ssh pi@YOUR_IP_HERE` enter your new password

