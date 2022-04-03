from flask import Flask, request
import time


app = Flask(__name__)

@app.route('/time')
def get_curr_time():
    return {'time': time.time()}

@app.route('/run', methods=['POST'], strict_slashes=False)
def run():
    pass
