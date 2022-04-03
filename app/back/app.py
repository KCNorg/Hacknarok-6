from flask import Flask, request, jsonify
import time


app = Flask(__name__)

@app.route('/time')
def get_curr_time():
    return {'time': time.time()}

@app.route('/send_values', methods=['POST'], strict_slashes=False)
def send_values():
    data = request.json
    print(data)
    return {'lng': 60, 'lat': 56}

# @app.route('/add_point')

# @app.route('/remove_point')

# @app.route('/show_tag')

# @app.route('/run')
