import pprint
import json
import requests
from flask import Flask, request
app = Flask(__name__)
# app.config['SERVER_NAME']=None
# app.config['SERVER_NAME']='danielkappelle.com'

webhook_url = "https://platform.etv.tudelft.nl/hooks/"


@app.route("/")
def hello():
        return "Hello World!"

@app.route("/hooks/<hook>",methods=['GET', 'POST'])
def bla(hook):
        # try:
        #         # pprint(request)
        #         return request.get_json()
        # except:
        #         return "no"
        # pprint.pprint(request)
        print request.get_json()["actor"]["username"]
        return "hoi"

if __name__ == "__main__":
        app.run(host='danielkappelle.com')
