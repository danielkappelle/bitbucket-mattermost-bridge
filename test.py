import pprint
import json
import requests
from flask import Flask, request
from pyxtension.Json import Json
app = Flask(__name__)

webhook_url = "https://platform.etv.tudelft.nl/hooks/"


@app.route("/")
def hello():
        return "Hello World!"

@app.route("/hooks/<hook>",methods=['GET', 'POST'])
def bla(hook):
        data = Json(request.get_json())

        repo = data.repository.full_name
        branch = data.push.changes[0].new.name
        commits = data.push.changes[0].commits
        actor = data.actor.username
        output = "[%s/%s] %d commits pushed by %s" % (repo, branch, len(commits), actor)
        for commit in commits:
            commithash = commit.hash
            link = commit.links.html.href
            author = commit.author.user.username
            message = commit.message.strip()
            output += "\n"
            output += "- [%s](%s) %s - %s" % (commithash[:7], link, message, author)
        # print(output)
        submitHook("https://platform.etv.tudelft.nl/hooks/%s" % hook, output)
        return "hoi"

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
