from flask import Flask, request
import time
import main
import json


app = Flask(__name__)


@app.route('/time')
def get_curr_time():
    return {'time': time.time()}


@app.route('/run', methods=['POST'], strict_slashes=False)
def run():
    res = main.main()
    return json.dumps(res), 200, {'ContentType': 'application/json'} 
