# Home Assistant - Pi Continuously Cast

Introduction:
============

**If you would prefer this functionality as an integration that runs on your HA instance, find this [here](https://github.com/b0mbays/ha-continuous-casting-dashboard), The guide below requires an external Linux box.**

Home Assistant Cast (_HA-Pi-Cast_) will continuously cast your Home Assistant dashboard to your Google Chromecast device; only if there is no media playing (or HA is already being casted) and the local time is between the defined "allowed casting time" to save some power overnight. 

I'm using this myself for 3 different chromecast devices: Lenovo Smart Display 8 & two 1st Gen Google Nest Hubs.
<p align="center">
  <img src="https://i.imgur.com/U63Z7aF.jpg" width=75% height=75%>
</p>
<br/><br/>

## How does it work?

The project uses [CATT](https://github.com/skorokithakis/catt) (cast all the things) to cast the dashboard to your Chromecast compatible device. Home Assistant does offer an in-built casting option but I found this to be unreliable for me and I couldn't get it working properly without paying for a Nabu Casu subscription... Instead, I wanted to host HA externally myself for free. (well, $1 p/year). The guide I used is [here](https://www.makeuseof.com/secure-home-assistant-installation-free-ssl-certificate/?newsletter_popup=1) and I bought a domain for $1 from [here](https://gen.xyz/).

HA-Cast is intended to be ran as a system service on a Linux box. I'm running it on a Raspberry Pi Zero, but any Linux box should do. This service will then iterate over your devices defined inside the config.yaml file every 10 seconds checking the 'status' of each device. We check the status using [CATT](https://github.com/skorokithakis/catt) and will only cast the dashboard if no media is playing or the dashboard is already being casted. This means that any spotify/youtube sessions won't be interupted, and when you end the "playing" session with "Hey Google, Stop" the dashboard will return.

<br/><br/>

Requirements: 
============
1. **Home Assistant** (with https [external access setup](https://www.makeuseof.com/secure-home-assistant-installation-free-ssl-certificate/?newsletter_popup=1) required for casting)
2. **Raspberry Pi** (or some other linux box... I'm using a Raspberry Pi Zero)
3. **Git** installed on your Linux box prior to starting the installation steps.
4. **Trusted network setup** for each Chromecast device to avoid logging in. See guide [here](https://blog.fuzzymistborn.com/homeassistant-and-catt-cast-all-the-things/) and follow the 'Trusted Networks' section half way down. You can either do your entire home network, or individual devices. You can find the IP address for each device by going to Settings -> Device Information -> Technical Information on the device.
5. **ha-catt-fix** setup for your dashboard to keep the display 'awake' and not time out after 10 minutes. Install this from [here](https://github.com/swiergot/ha-catt-fix)

<br/><br/>

Installation:
============
1. Clone this repo to: /opt/ha-cast:

```
sudo git clone https://github.com/b0mbays/ha-cast.git /opt/ha-cast
```

2. Update the 'config.yaml' file with your Chromecast device names and IP addresses:

```
sudo nano /opt/ha-cast/config.yaml
```

3. Execute setup.sh - This will install any requirements, setup a new system user and start the service and also ensure it starts on boot:

```
sudo bash /opt/ha-cast/setup.sh
```

Your devices should now start displaying your HA Dashboards! 

If you try to play Spotify/Youtube the dashboard will be hidden and will only return after a "Hey Google, Stop" (This may take up to 30 seconds depending how many devices you have)

<br/><br/>

Configuration:
============

* Allowed casting times:

The service will by default continuously try to cast to your chromecast devices between 06.30am -> 02.00am. (There will also be a 5 minute pause at 23.59pm). You can change these timings yourself if you like inside the **ha-cast.py** file on line 70.

* Devices:

You can setup your Google Chromecast Compatible devices inside the **config.yaml** under **device_map**. There's an example in there too.

* Cast Delay:

The default is set to 10 seconds for checking each device, you can change this inside the **config.yaml** under **cast_delay**.

```yaml
cast_delay: 10
device_map:
  "<YOUR_DISPLAY_NAME>": "YOUR_DASHBOARD_URL"
  "<YOUR_DISPLAY_NAME>": "YOUR_DASHBOARD_URL"
  "<YOUR_DISPLAY_NAME>": "YOUR_DASHBOARD_URL"
  # eg: "Office display": "http://192.168.12.104:8123/office-dashboard/default_view?kiosk"
  # eg: "Kitchen display": "http://192.168.12.104:8123/kitchen-dashboard/default_view?kiosk"
```


<br/><br/>

Debugging:
============

There is a log file: /opt/hacast/ha-cast.log that you can check for any errors that may occur.

```
cat /opt/ha-cast/ha-cast.log
```

Check the system status of the service with:

```
sudo systemctl status hacast
```

Restart the service:

```
sudo systemctl restart hacast
```

Disable the service on boot:

```
sudo systemctl disable hacast
```

Enable the service on boot:
```
sudo systemctl enable hacast
```


