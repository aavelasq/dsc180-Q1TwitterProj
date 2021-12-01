import json
import pandas as pd

def import_test_data(test_dir, file_dir):
    '''
    used for test target
    '''
    with open(test_dir) as f:
        json_file = json.load(f)
    df = pd.DataFrame(json_file['data'])
    return df

def import_data(test_dir, file_dir):
    '''
    used for data target
    '''
    # if data file is json format 
    # with open(file_dir) as f:
    #     json_file = json.load(f)

    # df = pd.DataFrame(json_file['data'])

    # if data file is csv format
    df = pd.read_csv(file_dir)
    return df