import sys
import json

sys.path.insert(0, 'src') # add src to paths

import etl
from eda import calculate_stats
from eda_q2 import research_q2

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
        research_q2(data)


    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        data = etl.import_test_data(**data_cfg)

        # rq 1 function
        calculate_stats(data, test=True)

        # rq 2 function
        research_q2(data, test=True)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)