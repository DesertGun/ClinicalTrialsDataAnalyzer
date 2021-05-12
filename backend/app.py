from flask import Flask, jsonify
from flask_cors import CORS
import threading
from update_database import download_data
import time
import datetime
import re
import glob


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



@app.before_first_request
def activate_update_job():

    

    
    def run_job():
        # TODO: Get File List and filter the raw-file
        # TODO: Remove Old raw-File after Update

        date_pattern = re.compile(r"_(\d+\d+\d+).csv")

        filename = "input_data_raw_12122020.csv"

        date_from_filename = date_pattern.search(filename).group(1)

        print(date_from_filename)

        date_of_today = datetime.datetime.now()
        date_of_database = datetime.datetime.strptime(date_from_filename, '%d%m%Y')
        date_diff = date_of_database - date_of_today

        if abs(date_diff.days) >= 7:
            update_needed = True

            while update_needed:
                print("Run update task")
                download_data()
                update_needed = False
                time.sleep(3)
        else:
            print("No Update Needed")

    thread = threading.Thread(target=run_job)
    thread.start()

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()