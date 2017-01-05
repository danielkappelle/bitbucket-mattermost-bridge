########################################
#   Bitbucket Mattermost Bridge        #
#                                      #
#   Written by Daniel Kappelle, 2016   #
########################################

#import modules
import json
import requests
from flask import Flask, request
from pyxtension.Json import Json
from jinja2 import Template
import os.path

#import user config
import config
from helpers import create_user_link

# Initialize flask app
app = Flask(__name__)

# Folder for the template files
template_folder = "templates/"


@app.route("/")
def renderHomePage():
    return "<h1>Bitbucket Mattermost Bridge</h1><p>Please refer to the repo on <a href='https://github.com/danielkappelle/bitbucket-mattermost-bridge'>Github</a> for the Readme.</p>"

@app.route("/hooks/<hook>",methods=['GET', 'POST'])
def bridgeHook(hook):
        # This function does all the magic

        # The event key is used to determine the type of event
        # e.g. repo:push, issue:created, etc.
        event = request.headers.get('X-Event-Key')

        # The template folder is searched for a template file
        # that matches thee event-key, (: replaced by -), e.g.
        # repo-push
        template_file_name = event.replace(":", "-")
        template_file = template_folder + template_file_name
        if(os.path.exists(template_file)):
            # Parse the json data from the webhook
            data = Json(request.get_json())
            user_link = create_user_link(data)

            # Read the template file and render it using the
            # data from the webhook
            template = Template(open(template_file, 'r').read())
            output = template.render(data=data, user_link=user_link)

            # Submit the new, bridged, webhook to the mattermost
            # incoming webhook
            submitHook(config.webhook_url + hook, output)
            return "Done"
        else:
            # In case there's no templat for the event
            # throw an error
            return "Couldn't handle this event", 501

def submitHook(url, hook_data):
    # This function submits the new hook to mattermost
    data = {'text':hook_data}
    
    # Post the webhook
    response = requests.post(
            url, data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
                )
    if response.status_code != 200:
        raise ValueError(
                        'Request to mattermost returned an error %s, the response is:\n%s'
                        % (response.status_code, response.text)
                        )

if __name__ == "__main__":
        # Run flask app on host, this is set in config.py
        app.run(host=config.host, port=config.port)
