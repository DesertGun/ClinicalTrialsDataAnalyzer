from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import threading, time, datetime, re, glob, os
from update_database import download_data
from ner_processing import create_results
import pandas as pd
import json


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


'''
@author Ervin Joa

If the first API call of the server session is 
made, the following method will, in a separate
thread, check if an update of the database is needed, in 
which case download it, label it and create a csv file 
for further operations, otherwise it will continue directly.

@return: none
'''
@app.before_first_request
def activate_update_job():

    def run_job():

        rootdir = "./"
        regex = re.compile(r"input_data_raw_(\d+\d+\d+).csv")
        filename = ""

        for root, dirs, files in os.walk(rootdir):
            for file in files:
                if regex.match(file):
                    filename = file

        date_pattern = re.compile(r"_(\d+\d+\d+).csv")
        date_from_filename = date_pattern.search(filename).group(1)

        print(date_from_filename)

        date_of_today = datetime.datetime.now()
        date_of_database = datetime.datetime.strptime(date_from_filename, '%m%d%Y')
        date_diff = date_of_database - date_of_today

        if abs(date_diff.days) >= 21:
            update_needed = True

            while update_needed:
                print("Run update task")
                # download_data()
                create_results()
                update_needed = False
                # os.remove(filename) 
                time.sleep(3)
                print("Finished updates")
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


'''
@author Ervin Joa

The following API call returns the processed 
data, either as a whole or filtered, depending 
on the user input.

@return: json(orient=records)
'''
@app.route('/filter', methods=['POST'])
def filter():
    empty = b'{"Change":"","Variable":"","Reference":"","Condition":"","Timepoint":"","GroupByOptions":[], "EndpointArt":""}'
    params_json = request.data
    print(params_json)

    
    if params_json != empty:
        result = result_data.copy()
        params_data  = json.loads(params_json)
        values = params_data.items()

        aggregation_filters = []
        group_by_options = []

        for key, value in values:
            if value and key == "Change":
                result = result[result[key]==value]
            elif value and key == "Reference":
                result = result[result[key]==value]
            elif value and key == "Condition":
                result = result[(result[key].str.contains(value.lower()))|
                (result[key].str.contains(value.capitalize()))|
                (result[key].str.contains(value))]
            elif value and key == "Timepoint":
                result = result[result[key]==value]
            elif value and key == "Variable":
                result = result[result[key]==value]
            elif value and key == "EndpointArt":
                result = result[result["Endpoint Art"]==value]
            elif key == "GroupByOptions" and value != []:
                for groupByVal in value: 
                    group_by_options.append(groupByVal)

                if "Endpoint Art" not in group_by_options:
                    group_by_options.extend(["Endpoint Art"])
                result = result.groupby(by=group_by_options).size().reset_index(name='Counts')
                
        if group_by_options:
            print(result.head())
            return result.sort_values(by=["Counts"], ascending = False).to_json(orient="records")
        else:
            print(result.head())
            return result.to_json(orient="records")
        
    else:
        return result_data.to_json(orient="records")

if __name__ == '__main__':
    app.run()