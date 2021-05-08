from flask import Flask, jsonify
from flask_cors import CORS
import threading
from update_database import download_data
import time


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.before_first_request
def activate_update_job():
    update_needed = True
    def run_job():
        while update_needed:
            print("Run update task")
            # TODO: Destinction whether the data is still valid or needs to be downloaded
            download_data()
            update_needed = False
            time.sleep(3)

    thread = threading.Thread(target=run_job)
    thread.start()

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()