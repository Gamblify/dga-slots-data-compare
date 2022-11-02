import os
import argparse

import time

import pprint

import safe
import csc

parser = argparse.ArgumentParser()

parser.add_argument('--safe-dir',  required=True, help='Directory with all the SAFE EndOfDay reports')
parser.add_argument('--csc-dir',  required=True, help='Directory with all the CSC reports')
parser.add_argument('--csc-extension', default='msg', help='File extensions for the CSC files')
parser.add_argument('--safe-extension', default='xml', help='File extensions for the SAFE files')
# parser.add_argument('--start-date', required=True, help='Start date in the format YYYYMMDD')
# parser.add_argument('--end-date', required=True, help='End date in the format YYYYMMDD')

try:
    args = parser.parse_args()
    csc_data = []
    # start_time = time.time()
    with os.scandir(args.csc_dir) as it:
        for entry in it:
            if entry.name.endswith(f'.{args.csc_extension}'):
                # print(f'Processing CSC file {entry.path}')
                csc_data.extend(csc.parse_csc_file(entry.path))
                # print(entry.path)
                # pprint.pprint(csc_data[-1])

    csc_by_date = csc.group_data(csc_data)

    # print("--- %s seconds ---" % (time.time() - start_time))

    safe_data = []
    with os.scandir(args.safe_dir) as it:
        for entry in it:
            if entry.name.endswith(f'.{args.safe_extension}'):
                safe_data.append(safe.parse_safe_file(entry.path))
                # print(entry.path)
                # pprint.pprint(safe_data[-1])

    # pprint.pprint(csc_data[:10])
    # print('-----' * 20)
    # pprint.pprint(safe_data[:10])
except Exception as e:
    print(e)

