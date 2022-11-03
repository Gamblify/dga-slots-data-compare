import argparse
import os
import sys
from datetime import datetime

import time

import pprint

import safe
import csc

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
parser.add_argument('-d', '--debug', action='store_true', help='Show debug log')
parser.add_argument('--safe-dir',  required=True, help='Directory with all the SAFE EndOfDay reports')
parser.add_argument('--csc-dir',  required=True, help='Directory with all the CSC reports')
parser.add_argument('--start-date', required=True,
                    type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Start date in the format YYYY-MM-DD')
parser.add_argument('--end-date', default=datetime.now().date(),
                    type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                    help='End date in the format YYYY-MM-DD. If not provided it will be today')
parser.add_argument('--csc-extension', default='msg', help='File extensions for the CSC files')
parser.add_argument('--safe-extension', default='xml', help='File extensions for the SAFE files')


try:
    args = parser.parse_args()

    v_print = print if args.verbose else lambda *a, **k: None
    d_print = print if args.debug else lambda *a, **k: None

    if args.start_date > args.end_date:
        sys.stderr.write('Start date should be before end date')
        sys.exit(1)

    csc_data = []
    start_time = time.time()
    v_print(f'Starting to parse CSC files in {args.csc_dir}')
    with os.scandir(args.csc_dir) as it:
        for entry in it:
            if entry.name.endswith(f'.{args.csc_extension}'):
                v_print(f' Processing CSC file {entry.path}')
                csc_data.extend(csc.parse_csc_file(entry.path))
                # print(entry.path)
                # pprint.pprint(csc_data[-1])
    d_print("--- CSC files parse time %s seconds ---" % (time.time() - start_time))

    csc_by_date_location = csc.group_data(csc_data)
    # pprint.pprint(csc_by_date_location)
    pprint.pprint(list(csc_by_date_location.items())[0])

    v_print(f'Starting to parse SAFE files in {args.safe_dir}')
    start_time = time.time()
    safe_data = {}
    with os.scandir(args.safe_dir) as it:
        for entry in it:
            if entry.name.endswith(f'.{args.safe_extension}'):
                v_print(f' Processing SAFE file {entry.path}')
                # print(entry.path)
                # pprint.pprint(report_date)
                # pprint.pprint(location_data)
                report_date, location_data = safe.parse_safe_file(entry.path)
                safe_data[report_date] = location_data

    d_print("--- SAFE files parse time %s seconds ---" % (time.time() - start_time))

    # pprint.pprint(safe_data)
    pprint.pprint(list(safe_data.items())[0])

except Exception as e:
    print(e)

