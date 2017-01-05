import os
# Config file, please set the following settings:

# host the bridge is listening for, default: localhost
host = os.environ.get('BRIDGE_LISTEN_ADDR', 'localhost')

# listening port, default 5000
port = os.environ.get('BRIDGE_LISTEN_POST', 5000)

# url to post bridged webhooks to, default
webhook_url = os.environ.get('MATTERMOST_HOOK')
if not webhook_url:
    raise Exception('You need to set MATTERMOST_HOOK environment variable')
