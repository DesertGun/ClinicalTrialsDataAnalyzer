import pandas as pd
import numpy as np



#def process_data(preprocessed_input_data):
#    data_pre_processed = pd.read_csv(preprocessed_input_data)
#    return processed_resultsDF

def export_results(processed_resultsDF):
    # Following function creates the result csv and returns
    
    export = processed_resultsDF
    export.to_csv("results.csv")
