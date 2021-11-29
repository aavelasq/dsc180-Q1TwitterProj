import json
import pandas as pd

def import_test_data(test_dir, file_dir):
    with open(test_dir) as f:
        json_file = json.load(f)
    df = pd.DataFrame(json_file['data'])
    return df

def import_data(test_dir, file_dir):
    with open(file_dir) as f:
        json_file = json.load(f)

    df = pd.DataFrame(json_file['data'])
    return df