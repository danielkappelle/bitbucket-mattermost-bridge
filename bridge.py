import pprint
import json
import requests
from flask import Flask, request
from pyxtension.Json import Json
from jinja2 import Template
import os.path
app = Flask(__name__)

webhook_url = "https://platform.etv.tudelft.nl/hooks/"
template_folder = "templates/"


@app.route("/")
def hello():
        return "Hello World!"

@app.route("/hooks/<hook>",methods=['GET', 'POST'])
def bla(hook):
        event = request.headers.get('X-Event-Key')
        template_file_name = event.replace(":", "-")
        template_file = template_folder + template_file_name
        if(os.path.exists(template_file)):
            template = Template(open(template_file, 'r').read())
	    data = Json(request.get_json())
	    output = template.render(data=data)
            submitHook("https://platform.etv.tudelft.nl/hooks/%s" % hook, output)
            return "Done"
        else:
            return "Couldn't handle this event"

def submitHook(url, hook_data):
    data = {'text':hook_data}
    
    response = requests.post(
            url, data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
                )
    if response.status_code != 200:
        raise ValueError(
                        'Request to slack returned an error %s, the response is:\n%s'
                        % (response.status_code, response.text)
                        )

if __name__ == "__main__":
        app.run(host='danielkappelle.com')
