
Edit `/etc/wpa_supplicant/wpa_supplicant.conf`

Add WiFi network name and password:

add the following to whatever is already in the file:

```
country=US

network={
    ssid="testing"
    psk="testingPassword"
}
```

Run:
```
sudo /etc/init.d/networking restart
```


For troubleshooting see:
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
