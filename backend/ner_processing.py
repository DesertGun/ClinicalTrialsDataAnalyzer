import spacy, random
from spacy.util import minibatch, compounding
from spacy.training import Example
import pandas as pd

# Loading the Model
nlp = spacy.load("../training/ner_model")


def create_results():
    

    # Loading the input_data
    data = pd.read_csv("input_data_filtered.csv")

    # Converting the features into strings
    data["PrimaryOutcomeMeasure"] = data["PrimaryOutcomeMeasure"].astype(str)
    data["PrimaryTimeFrame"] = data["PrimaryTimeFrame"].astype(str)
    data["SecondaryOutcomeMeasure"] = data["SecondaryOutcomeMeasure"].astype(str)
    data["SecondaryTimeFrame"] = data["SecondaryTimeFrame"].astype(str)

    results_df = data_to_dataframe(data)

    results_df = results_df[(results_df["Change"] != "Not Mentioned") & (results_df["Variable"] != "Not Mentioned") &
                        (results_df["Reference"] != "Not Mentioned") & (results_df["Timepoint"] != "Not Mentioned")]

    export = results_df
    export["Condition"] = export["Condition"].str.title()
    export["Reference"] = export["Reference"].str.title()
    export["Variable"] = export["Variable"].str.title()
    export["Timepoint"] = export["Timepoint"].str.title()
    export["Change"] = export["Change"].str.title()

    export = export.fillna('Not Mentioned')
    export.rename_axis("Index", axis='index', inplace=True)
    export.to_csv("results.csv")


def data_to_dataframe(data):
    dfTest = pd.DataFrame(columns=["NCTId","Condition","Change","Reference", "Variable", "Timepoint"])

    for index, row in data.iterrows():
        pointer = 0
        trial_id = row[1]

        condition = row[2]
        
        primary_endpoint = row[3]
        primary_endpoints = []

        primary_endpoint_timepoint = row[4]
        primary_endpoint_timepoints = []

        secondary_endpoint = row[5]
        secondary_endpoints = []

        secondary_endpoint_timepoint = row[6]
        secondary_endpoint_timepoints = []
        
        if  primary_endpoint.find("|") != -1:
            primary_endpoints = primary_endpoint.split("|")

        if  primary_endpoint_timepoint.find("|") != -1:
            primary_endpoint_timepoints = primary_endpoint_timepoint.split("|")

        if  secondary_endpoint.find("|") != -1:
            secondary_endpoints = secondary_endpoint.split('|')

        if  secondary_endpoint_timepoint.find("|") != -1:
            secondary_endpoint_timepoints = secondary_endpoint_timepoint.split('|')
        
        if primary_endpoints == []:
            endpoint_art = "Primary Endpoint"
            dfTemp = process_text_entry(trial_id, condition, primary_endpoint, endpoint_art, pointer, primary_endpoint_timepoint)
            dfTest = dfTest.append(dfTemp, ignore_index= True)
        else:
            for point, timepoint in zip(primary_endpoints, primary_endpoint_timepoints):
                endpoint_art = "Primary Endpoint"
                dfTemp = process_text_entry(trial_id, condition, point, endpoint_art, pointer, timepoint)
                dfTest = dfTest.append(dfTemp, ignore_index= True)


        if secondary_endpoints == []:
            endpoint_art="Secondary Endpoint"
            dfTemp = process_text_entry(trial_id, condition, secondary_endpoint, endpoint_art, pointer, secondary_endpoint_timepoint)
            dfTest = dfTest.append(dfTemp, ignore_index= True)
        else:
            for point, timepoint in zip(secondary_endpoints, secondary_endpoint_timepoints):
                endpoint_art = "Secondary Endpoint"
                dfTemp = process_text_entry(trial_id, condition, point,endpoint_art, pointer, timepoint)
                dfTest = dfTest.append(dfTemp, ignore_index= True)
                pointer+=1

    return dfTest


# TODO: If multiple equal labels they must be concatinated
# TODO: Update training params, for training to be as short as possible 
def process_text_entry(nctid, condition, text, endpoint_art, pointer, timepoint):
    dfTemp = pd.DataFrame(columns=["NCTId","Condition","Change","Reference", "Variable", "Timepoint", "Endpoint Art"])

    target = nlp(text)
    for entity in target.ents:
        dfTemp.at[pointer,"NCTId"]=nctid
        dfTemp.at[pointer,"Condition"]=condition
        if entity.label_ != "Condition":
            dfTemp[entity.label_]=entity.text
        dfTemp.at[pointer,"Endpoint Art"]=endpoint_art
        if entity.label_ != "Timepoint":
            dfTemp.at[pointer, "Timepoint"] = timepoint
    return dfTemp

