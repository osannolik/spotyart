# Target
Raspberry pi with Hyperpixel 4.0

raspberry pi os

# Setup

It's a bit manual.

## Spotipy

The application uses Spotify's web API. This means that you need to create an app on the Spotify dashboard, and put the app credentials in ```auth.sh```. For more info read the [documentation](https://developer.spotify.com/documentation/web-api). First time running the application you need to authorize yourself using a browser, so do a manual start:

```shell
> source auth.sh
> python spotify_client.py
```

## Display brightness

Brightness is set using [pigpio](https://abyz.me.uk/rpi/pigpio/) and its hardware PWM interface since that reduces backlight flickering. The application assumes that its daemon ```pigpiod``` is running. To make sure it is always started during boot enable its systemd service:

```shell
> sudo systemctl enable pigpiod.service
```

It could also be helpful to turn off display blanking in raspberry pi os:

```shell
> sudo raspi-config
```

## Startup during boot

The application can be started simply by running ```start.sh```, but its way more nice to have it started automatically at boot. Make sure to edit ```start.sh``` to set the path to the source files.

```shell
> mkdir -p ~/.config/systemd/user/
> cp cool-user-display.service ~/.config/systemd/user/
> systemctl --user daemon-reload
> systemctl --user enable cool-user-display.service
```

Reboot is needed.

# Requirements

Run and find out.
