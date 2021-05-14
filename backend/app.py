from flask import Flask, jsonify
from flask_cors import CORS
import threading, time, datetime, re, glob
from update_database import download_data
from data_process import export_results
import pandas as pd


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



@app.before_first_request
def activate_update_job():

    def run_job():
        # TODO: Get File List and filter the raw-file
        # TODO: Remove Old raw-File after Update

        date_pattern = re.compile(r"_(\d+\d+\d+).csv")

        filename = "input_data_raw_05122021.csv"

        date_from_filename = date_pattern.search(filename).group(1)

        print(date_from_filename)

        date_of_today = datetime.datetime.now()
        date_of_database = datetime.datetime.strptime(date_from_filename, '%m%d%Y')
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

result_data = pd.read_csv('./results.csv')
# TODO: Check if Data is present
# TODO: If Not then Frontend should show warning
@app.route('/results', methods=['GET'])
def send_results():
    print(result_data.head())
    return result_data.to_json(orient="records")

if __name__ == '__main__':
    app.run()