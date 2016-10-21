# Gitbucket mattermost bridge
This tool converts the bitbucket webhook request so that mattermost can interpret it properly.

# Installation
This installation guide is based on `Ubuntu 14.04` with `Python 2.7` and `pip` installed.

## Clone repo
`$ git clone https://github.com/danielkappelle/bitbucket-mattermost-bridge`

## Install dependencies
`$ pip install -r requirements.txt`

## Edit config
Copy the config sample and edit
`$ cp config.py.sample config.py`
`$ vim config.py` or `$ nano config.py` (or whatever editor you prefer)

Enter your hostname, port and the url to the mattermost instance

## Run the bridge
### Directly
This can be useful for debugging
`$ python bridge.py`

### As a daemon
If you don't have already installed upstart:
```
$ sudo apt-get update
$ sudo apt-get install upstart
```

Create the upstartfile
`$ vim /etc/init/bitbucket-mattermost-bridge.conf` (or nano, or gedit...)

```
description "Bitbucket mattermost integration"
author  "Daniel Kappelle <daniel.kappelle@gmail.com>"

start on runlevel [234]
stop on runlevel [0156]

chdir /home/daniel/programming/bitbucket-mattermost-bridge/
exec python /home/daniel/programming/bitbucket-mattermost-bridge/bridge.py
respawn
```

You can now start/stop/restart the daemon using
`$ sudo start|stop|restart bitbucket-mattermost-bridge`

# Trouble
If there's any trouble, please contact me or create an issue
