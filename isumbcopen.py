import requests
import pyalexa
import flask
import json
import time

BASE_RESPONSE = {
    "version": "1",
    "response": {}
}

with open(".alexa_keys") as f:
    keys = json.load(f)

TWITTER_APP_KEY = keys["api_key"]
TWITTER_APP_KEY_SECRET = keys["api_secret"]
TWITTER_ACCESS_TOKEN = keys["access_token"]
TWITTER_ACCESS_TOKEN_SECRET = keys["token_secret"]

APP_ID = keys["app_id"]

CACHE_TIME = 300

api = flask.Flask(__name__)

skill = pyalexa.Skill(app_id=APP_ID)

status = "UHH"
last_update = 0

def get_status():
    if time.time() > last_update + CACHE_TIME:
        global status
        try:
            res = requests.get("http://isumbcopen.com/api")
            if res and res.status_code and res.status_code == 200:
                status = res.text.strip()
                global last_update
                last_update = time.time()
        except:
            pass

    return status

@skill.launch
def launch(request):
    return request.response(end=True, speech=get_status())

@skill.end
def end(request):
    return request.response(end=True)

get_status()

api.add_url_rule('/', 'pyalexa', skill.flask_target, methods=['POST'])
api.run('0.0.0.0', port=8083, debug=False)
