import pprint
from collections import defaultdict
from datetime import datetime, timedelta


def parse_csc_start_record(start_record: str):
    assert start_record.startswith(' ' * 6), 'Bad start padding for CSC record: ' + start_record
    start_record = start_record[6:]
    # TODO use start_record when start_date and end_date are being used
    pass


def parse_csc_record(csc_record: str):
    ret_dict = {}

    assert csc_record.startswith(' ' * 6), 'Bad start padding for CSC record: ' + csc_record
    csc_record = csc_record[6:]

    assert csc_record.endswith(' ' * 8), 'Bad end padding for CSC record: ' + csc_record
    csc_record = csc_record[:-8]

    assert csc_record.startswith('01'), 'Bad constant for CSC record: ' + csc_record
    csc_record = csc_record[2:]

    ret_dict['locationMainNumber'] = csc_record[:8]
    csc_record = csc_record[8:]

    ret_dict['machineName'] = csc_record[:12].rstrip(' ')
    csc_record = csc_record[12:]

    ret_dict['datetime'] = datetime.strptime(csc_record[:14], '%Y%m%d%H%M%S')
    csc_record = csc_record[14:]

    ret_dict['firmwareName'] = csc_record[:16].rstrip(' ')
    csc_record = csc_record[16:]

    ret_dict['firmwareVersion'] = csc_record[:10].rstrip(' ')
    csc_record = csc_record[10:]

    ret_dict['moneyInserted'] = int(csc_record[:17])
    csc_record = csc_record[17:]

    ret_dict['moneyPaidOut'] = int(csc_record[:17])
    csc_record = csc_record[17:]

    ret_dict['moneyPlayed'] = int(csc_record[:17])
    csc_record = csc_record[17:]

    ret_dict['moneyWon'] = int(csc_record[:17])
    csc_record = csc_record[17:]

    ret_dict['firmwareChecksum'] = csc_record[:8].rstrip(' ')
    csc_record = csc_record[8:]

    # print(csc_record)
    # pprint.pprint(ret_dict)

    assert len(csc_record) == 0, 'CSC Record has more characters than needed: ' + csc_record

    return ret_dict


def parse_csc_end_record(end_record: str):
    assert end_record.startswith(' ' * 6), 'Bad start padding for CSC End record: ' + end_record
    end_record = end_record[6:]

    assert end_record.startswith('10'), 'Bad start constant for CSC End Record: ' + end_record
    end_record = int(end_record[2:])

    return end_record


def parse_csc_lines(start_record: str, end_record: str, csc_records: list):
    parse_csc_start_record(start_record)
    number_of_records = parse_csc_end_record(end_record)
    parsed_records = []

    for record in csc_records:
        parsed_records.append(parse_csc_record(record))

    # pprint.pprint(csc_records[:10])
    assert number_of_records == len(parsed_records), f'Length mismatch of reported len({number_of_records}), and ' \
                                                     f'records_len({len(parsed_records)}'

    return parsed_records


def parse_csc_file(csc_filename: str):
    csc_records = []
    start_csc_record = 'N/A'
    end_csc_record = 'N/A'

    with open(csc_filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace('\n', '')
            if line.lstrip().startswith('00'):
                start_csc_record = line
            elif line.lstrip().startswith('10'):
                end_csc_record = line
            else:
                csc_records.append(line)

    # print(start_csc_record)
    # pprint.pprint(csc_records[:10])
    # print(end_csc_record)

    return parse_csc_lines(start_csc_record, end_csc_record, csc_records)


def minmax_time_diff(machine_data: list):
    assert len(machine_data) != 0, "There is no data for machine"

    min_v = max_v = machine_data[0]

    for val in machine_data:
        if val['datetime'] < min_v['datetime']:
            min_v = val

        if val['datetime'] > max_v['datetime']:
            max_v = val

    # print(max_v, min_v)
    return min_v, max_v


def split_by_location(csc_records: list):
    data_by_location = defaultdict(list)

    for record in csc_records:
        data_by_location[record['locationMainNumber']].append(
            {k: record[k] for k in record if k != 'locationMainNumber'}
        )

    # pprint.pprint(list(data_by_location.keys())[:3])
    # pprint.pprint(list(data_by_location.items())[:1])

    data_by_machines = defaultdict(list)

    for k, v in data_by_location.items():
        machine_list = defaultdict(list)
        for record in v:
            machine_list[record['machineName']].append({k: v for k, v in record.items() if k != 'machineName'})
        # print(machine_list)
        data_by_machines[k] = dict(machine_list)

    # pprint.pprint(list(data_by_machines.keys())[:3])
    # pprint.pprint(list(data_by_machines.items())[:1])

    ret_value = {}

    for k, v in data_by_machines.items():
        # print(k)
        # pprint.pprint(v)

        total_money_inserted = 0
        total_money_paid_out = 0
        total_money_played = 0
        total_money_won = 0

        for machine_records in v.values():
            min_time_record, max_time_record = minmax_time_diff(machine_records)
            # print(min_time_record)
            # print(max_time_record)
            assert min_time_record['datetime'].hour == 0 and min_time_record['datetime'].minute == 0, \
                'min_time_record is not midnight record' + str(min_time_record)
            assert max_time_record['datetime'].hour == 0 and max_time_record['datetime'].minute == 0, \
                'max_time_record is not midnight record' + str(max_time_record)

            total_money_inserted += max_time_record['moneyInserted'] - min_time_record['moneyInserted']
            total_money_paid_out += max_time_record['moneyPaidOut'] - min_time_record['moneyPaidOut']
            total_money_played += max_time_record['moneyPaidOut'] - min_time_record['moneyPaidOut']
            total_money_won += max_time_record['moneyWon'] - min_time_record['moneyWon']

        ret_value[k] = {
            'moneyInserted': total_money_inserted,
            'moneyPaidOut': total_money_paid_out,
            'moneyPlayed': total_money_played,
            'moneyWon': total_money_won
        }

    # pprint.pprint(list(ret_value.keys())[:3])
    # pprint.pprint(list(ret_value.items())[:1])
    # pprint.pprint(ret_value['10022470'])
    # pprint.pprint(ret_value)

    return ret_value


def group_data(csc_data: list):
    data_by_date = defaultdict(list)
    td1_hour = timedelta(hours=1)

    for record in csc_data:
        # pprint.pprint(record)
        record_datetime = record['datetime']
        # new_value = {k: record[k] for k in record if k != 'datetime'}
        new_value = record
        data_by_date[record_datetime.date()].append(new_value)
        if record_datetime.time().hour == 0:
            assert record_datetime.time().minute == 0, "Record is not hourly: " + str(record)
            prev_day = record_datetime - td1_hour
            data_by_date[prev_day.date()].append(new_value)

    # pprint.pprint(list(data_by_date.keys())[:3])
    # pprint.pprint(list(data_by_date.items())[:1])

    ret_value = {}

    for k_date, k_values in data_by_date.items():
        ret_value[k_date] = split_by_location(k_values)

    # pprint.pprint(list(ret_value.keys())[:3])
    # pprint.pprint(list(ret_value.items())[:1])
    # pprint.pprint(ret_value)

    return ret_value
