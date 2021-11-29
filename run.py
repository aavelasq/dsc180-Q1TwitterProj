import sys
import json

sys.path.insert(0, 'src')

import etl
from eda import calculate_stats

def main(targets):
    # data_config = json.load(open('config/data-params.json'))

    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        data = etl.import_data(**data_cfg)

    if 'eda' in targets:
        calculate_stats(data)

    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        data = etl.import_test_data(**data_cfg)

        calculate_stats(data)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)