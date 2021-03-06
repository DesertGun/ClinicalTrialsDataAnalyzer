from numpy import nan
import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training import Example
import pandas as pd

# Loading the Model
nlp = spacy.load("../training/ner_model")

'''
@author Ervin Joa

The following method iterates over all rows of the 
database and creates the results of the tagging as a csv file.

@return: DateFrame as .csv file
'''


def create_results():

    # Loading the input_data
    data = pd.read_csv("input_data_filtered.csv")

    # Converting the features into strings
    data["PrimaryOutcomeMeasure"] = data["PrimaryOutcomeMeasure"].astype(str)
    data["PrimaryTimeFrame"] = data["PrimaryTimeFrame"].astype(str)
    data["SecondaryOutcomeMeasure"] = data["SecondaryOutcomeMeasure"].astype(
        str)
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
    export.replace({'Nan': nan}, inplace=True)
    export = export.fillna('Not Mentioned')

    export.rename_axis("Index", axis='index', inplace=True)
    export.to_csv("results.csv")


'''
@author Ervin Joa

The following method takes a DataFrame and processes 
individual features, per row, labels them and returns a DataFrame 
filled with the new labels.

@param data: DataFrame from clinicalTrials

@return: DateFrame
'''


def data_to_dataframe(data):
    df = pd.DataFrame(
        columns=["NCTId", "Condition", "Change", "Reference", "Variable", "Timepoint"])

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

        multiple_conditions = []

        if primary_endpoint.find("|") != -1:
            primary_endpoints = primary_endpoint.split("|")

        if primary_endpoint_timepoint.find("|") != -1:
            primary_endpoint_timepoints = primary_endpoint_timepoint.split("|")

        if secondary_endpoint.find("|") != -1:
            secondary_endpoints = secondary_endpoint.split('|')

        if secondary_endpoint_timepoint.find("|") != -1:
            secondary_endpoint_timepoints = secondary_endpoint_timepoint.split(
                '|')

        if condition.find("|") != -1:
            multiple_conditions = condition.split('|')

            end_condition = ", "
            end_condition_items = []

            for cond in multiple_conditions:
                end_condition_items.append(cond)

            end_condition = end_condition.join(end_condition_items)
            condition = end_condition

        if primary_endpoints == []:
            endpoint_art = "Primary Endpoint"
            df_temp = process_text_entry(
                trial_id, condition, primary_endpoint, endpoint_art, pointer, primary_endpoint_timepoint)
            df = df.append(df_temp, ignore_index=True)
        else:
            for point, timepoint in zip(primary_endpoints, primary_endpoint_timepoints):
                endpoint_art = "Primary Endpoint"
                df_temp = process_text_entry(
                    trial_id, condition, point, endpoint_art, pointer, timepoint)
                df = df.append(df_temp, ignore_index=True)
                pointer += 1

        if secondary_endpoints == []:
            endpoint_art = "Secondary Endpoint"
            df_temp = process_text_entry(
                trial_id, condition, secondary_endpoint, endpoint_art, pointer, secondary_endpoint_timepoint)
            df = df.append(df_temp, ignore_index=True)
        else:
            for point, timepoint in zip(secondary_endpoints, secondary_endpoint_timepoints):
                endpoint_art = "Secondary Endpoint"
                df_temp = process_text_entry(
                    trial_id, condition, point, endpoint_art, pointer, timepoint)
                df = df.append(df_temp, ignore_index=True)
                pointer += 1

    return df


'''
@author Ervin Joa

The following method takes a list of labels with
their corresponding text and if multiple keyword have
the same label, concatinates them into a single String.

@param target_list: list if target data (label: text)

@return: String
'''


def get_labels(target_list):
    label_list = []

    for el in target_list:
        if el.label_ == "Reference" or el.label_ == "Variable":
            label_list.append(el.text)

    label_list = list(set(label_list))

    label_str = ", ".join(map(str, label_list))
    return label_str


'''
@author Ervin Joa

The following method is responsible for labelling, which 
processes a single row of data. Care is taken to ensure that if 
neither time frame nor condition is found, then associated 
features are considered.

@param ncid: ID of the trial
@param condition: condition found in the data-row
@param enpoint_art: art of the endpoint found in the data-row
@param text: text corpus of the trials endpoint
@param pointer: pointer of the data, if multilined entry is present
@param timepoint: timepoint of the trials endpoint found

@return: DateFrame for the specific trial
'''


def process_text_entry(nctid, condition, text, endpoint_art, pointer, timepoint):
    df_temp = pd.DataFrame(columns=[
                          "NCTId", "Condition", "Change", "Reference", "Variable", "Timepoint", "Endpoint Art"])

    target = nlp(text)
    target_list = list(target.ents)

    label_str = get_labels(target_list)

    for entity in target.ents:
        df_temp.at[pointer, "NCTId"] = nctid
        df_temp.at[pointer, "Condition"] = condition
        if entity.label_ != "Condition":
            df_temp[entity.label_] = entity.text
        df_temp.at[pointer, "Endpoint Art"] = endpoint_art
        if entity.label_ == "Reference" or entity.label_ == "Variable":
            df_temp[entity.label_] = label_str
        if entity.label_ != "Timepoint":
            df_temp.at[pointer, "Timepoint"] = timepoint
    return df_temp
