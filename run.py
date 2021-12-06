import sys
import json

sys.path.insert(0, 'src') # add src to paths

import etl
from eda import calculate_stats

def main(targets):
    # data_config = json.load(open('config/data-params.json'))

    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        data = etl.import_data(**data_cfg)

    if 'eda' in targets:
        # rq 1 function 
        calculate_stats(data)

        # rq 2 function

    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        data = etl.import_test_data(**data_cfg)

        calculate_stats(data, test=True)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)