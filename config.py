import os
# Config file, please set the following settings:

# host the bridge is listening for, default: 0.0.0.0
host = os.environ.get('BRIDGE_LISTEN_ADDR', '0.0.0.0')

# listening port, default 5000
port = os.environ.get('BRIDGE_LISTEN_POST', 5000)

# url to post bridged webhooks to
webhook_url = os.environ.get('MATTERMOST_HOOK', '')
if not webhook_url:
    raise Exception('You need to set MATTERMOST_HOOK environment variable')

# Username showed in mattermost message
# "Enable Overriding of Usernames from Webhooks" must be turned on to work
username = os.environ.get('MATTERMOST_USERNAME', 'webhook')

# User icon showed in mattermost message
# "Enable Overriding of Icon from Webhooks" must be turned on to work
icon = os.environ.get('MATTERMOST_ICON', '')