# Continously Cast Home Assistant to a Google Chromecast device ##

## Introduction

This project will continuously cast your Home Assistant dashboard to your Google Chromecast device; only if there is no media playing (or HA is already being casted). I'm using this for 3 different chromecast devices (Lenovo Smart Display 8 & two Google Nest Hubs - 1st gen).

The project uses CATT (cast all the things) to cast the dashboard as I found the in-built HA Cast to not work well for me. Also, it seems I couldn't get it working properly without paying for a Nabu Casu subscription... Instead, I wanted to host HA externally myself for free. (well, $1 p/year). That guide is here. 

## Prerequesites 

1. Home Assistant (with https external access setup required for casting)
2. Raspberry pi (or some other linux box... I'm using a Raspberry Pi Zero)

## Installation

* Clone the repo to: /opt/hacast

```
sudo git clone https://github.com/b0mbays/ha-cast.git /opt/ha-cast
```

* Execute setup.sh - This will install any requirements, setup a new user and service and ensure it starts on boot.

```
sudo bash /opt/ha-cast/setup.sh
```

* Find your chromecast device names (and IP addresses which need to be added to HA's trusted network config so the device won't need to login!)

```
catt scan
```
Note down your device names and IP addresses and use nano to edit the ha-cat.py file

```
sudo nano /opt/ha-cast/ha-cast.py
```

Find the 'device_map' towards the top of the file, and amend the device names and IP addresses for all of your supported devices.

Restart the hacast.service:

```
sudo systemctl restart hacast
```

Your devices should now start displaying your HA Dashboards! If you try to play Spotify/Youtube the dashboard will vanish. However this will only return after you do a "Hey google, stop" (This may take up to 30 seconds or so depending how many devices you have)


## Debugging

There is a log file: /opt/hacast/ha-cast.log that you can check for any errors that may occur.


```
cat /opt/ha-cast/ha-cast.log
```
