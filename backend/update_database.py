import pandas as pd
import numpy as np
import time
import datetime




def get_new_chunk(current_border, tmp_border):
    print("Current Border: " + current_border + ", tmp_border: " + tmp_border)

    url_new_chunk="https://clinicaltrials.gov/api/query/study_fields?expr=Type+2+Diabetes&min_rnk=" + current_border +"&max_rnk="+tmp_border+"&fields=NCTId,Condition,OverallStatus,PrimaryOutcomeMeasure,PrimaryOutcomeTimeFrame,SecondaryOutcomeMeasure,SecondaryOutcomeTimeFrame,WhyStopped,BaselineMeasureTitle&fmt=csv"

    data_new_chunk = pd.read_csv(url_new_chunk,  skiprows = 11, names=["NCTId","Condition","OverallStatus","PrimaryOutcomeMeasure","PrimaryTimeFrame","SecondaryOutcomeMeasure","SecondaryTimeFrame", "WhyStopped", "BaselineMeasureTitle"])
    return data_new_chunk

def download_data():

    # retrieve the information of the data avalible

    url_info="https://clinicaltrials.gov/api/query/study_fields?min_rnk=1&max_rnk=1&fields=NCTId&fmt=csv"
    info = pd.read_csv(url_info, nrows=8, names=["art"])


    max_border = int(info.iloc[3]["art"].split(": ")[1])


    current_border = 1
    tmp_border = 1000
    input_data = pd.DataFrame(columns=["NCTId","Condition","OverallStatus","PrimaryOutcomeMeasure","PrimaryTimeFrame",
                                "SecondaryOutcomeMeasure","SecondaryTimeFrame", "WhyStopped"])


    # Phase 1: download the data and create a input_data.csv
    # get and concat the data, while the max_border not reached

    while tmp_border < max_border:

        # gets the new chunk from min_rnk:max_rnk
        input_data_current_chunk = get_new_chunk(str(current_border), str(tmp_border))

        # concat old state with new data_chunk
        concat_frames = [input_data, input_data_current_chunk] 

        new_data_merge = pd.concat(concat_frames)
        print("rows in Result_DF: " + str(len(new_data_merge)))

        # set new borders
        current_border = tmp_border
        tmp_border += 999
        # save and empty the tmp_df
        input_data = new_data_merge
        time.sleep(1)


    # the last < 1000 values will be retrieved by using new borders based on the diff.
    # TODO: False Logic couses ca. 900 extra repeated rows
    diff_border = max_border - current_border
    input_data_last_chunk = get_new_chunk(str(current_border), str(current_border + diff_border))

    concat_frames_final = [input_data, input_data_last_chunk] 
    input_data = pd.concat(concat_frames)

    # create input_data.csv
    date_new = datetime.datetime.now().strftime("%m%d%Y")
    input_data.to_csv("input_data_raw_" + date_new +".csv")
    filtered = input_data[(input_data["OverallStatus"] == "Completed") & (input_data["WhyStopped"].astype(str) == "nan")]
    export = filtered.drop(columns=["WhyStopped", "OverallStatus"], axis = 1)
    export[0:100].to_csv("input_data_filtered.csv")
    # TODO: Prototype will be using only 100 rows! In full version the whole data will be used