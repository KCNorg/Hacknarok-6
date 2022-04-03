from flask import Flask, request
import time


app = Flask(__name__)

@app.route('/time')
def get_curr_time():
    return {'time': time.time()}

@app.route('/send_values', methods=['POST'], strict_slashes=False)
def send_values():
    return request.json['name']

# @app.route('/add_point')

# @app.route('/remove_point')

# @app.route('/show_tag')

# @app.route('/run')
