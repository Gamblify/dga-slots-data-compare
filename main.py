import argparse
import os
import sys
from datetime import datetime, timedelta

import time

import pprint

import safe
import csc


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(days=n)


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
parser.add_argument('--csc-extension', default='msg', help='File extensions for the CSC files. default=msg')
parser.add_argument('--safe-extension', default='xml', help='File extensions for the SAFE files. default=xml')


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
    # pprint.pprint(list(csc_by_date_location.items())[0])

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
    # pprint.pprint(list(safe_data.items())[0])

    for single_date in daterange(args.start_date, args.end_date + timedelta(days=1)):
        if single_date not in csc_by_date_location:
            v_print(f'There is no data for in CSC for day {single_date}. Will not compare this date')
            continue

        if single_date not in safe_data:
            v_print(f'There is no data for in SAFE for day {single_date}. Will not compare this date')
            continue

        # print(single_date)
        # print(csc_by_date_location[single_date])
        # print(safe_data[single_date])
        csc_location_data = csc_by_date_location[single_date]
        safe_location_data = safe_data[single_date]

        union_location = set(csc_location_data.keys()).union(safe_location_data.keys())

        # pprint.pprint(union_location)

        for loc in union_location:
            if loc not in csc_location_data:
                v_print(f'There is no data for in CSC for location {loc}. Will not compare this location')
                continue

            if loc not in safe_location_data:
                v_print(f'There is no data for in SAFE for location {loc}. Will not compare this location')
                continue

            csc_comp_data = csc_location_data[loc]
            safe_comp_data = safe_location_data[loc]
            # CSC has 'moneyPlayed' and 'moneyWon' as data which is not compared
            # SAFE has 'numberOfPlays' and 'jackpotMoneyWon' as data which is not compared

            print(f'Comparing CSC and SAFE data for {single_date} for locationMainNumber: {loc}')
            if csc_comp_data['moneyInserted'] != safe_comp_data['moneyInserted']:
                print(f"\tDifferent 'moneyInserted' in CSC({csc_comp_data['moneyInserted']}) "
                      f"and SAFE({safe_comp_data['moneyInserted']}) ")
            else:
                print(f"\tSame 'moneyInsertedData'")

            if csc_comp_data['moneyPaidOut'] != safe_comp_data['moneyPaidOut']:
                print(f"\tDifferent 'moneyPaidOut' in CSC({csc_comp_data['moneyPaidOut']}) "
                      f"and SAFE({safe_comp_data['moneyPaidOut']}) ")
            else:
                print(f"\tSame 'moneyPaidOut'")


except Exception as e:
    print(e)

