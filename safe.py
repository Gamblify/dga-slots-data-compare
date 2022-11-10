import xmltodict
import pprint
from datetime import datetime


def get_entry_data(entry: dict):
    return {
            'locationMainNumber': entry['SpilstedHovednummer'],
            'numberOfPlays': int(entry['SpilstedEndOfDayRapportAntalSpil']),
            'moneyInserted': float(entry['SpilstedEndOfDayRapportIndskudTotal']),
            'moneyPaidOut': float(entry['SpilstedEndOfDayRapportGevinsterSpil']),
            'jackpotMoneyWon': float(entry['SpilstedEndOfDayRapportGevinsterJackpot'])
        }


def get_locations_info(locations_list: dict):
    ret_list = []
    # pprint.pprint(locations_list)

    if isinstance(locations_list, dict):
        return [get_entry_data(locations_list)]

    for entry in locations_list:
        # pprint.pprint(entry)
        ret_list.append(get_entry_data(entry))

    return ret_list


def parse_xml_dict(xml_dict: dict):
    data_dict = xml_dict['SpilleautomatEndOfDayStruktur']
    permit_dict = data_dict['Tilladelsesindehaver']

    # pprint.pprint(data_dict['SpecifiktSpilstedListe']['SpecifiktSpilsted'])

    locations_data = get_locations_info(data_dict['SpecifiktSpilstedListe']['SpecifiktSpilsted'])

    data_by_location = {}
    for entry in locations_data:
        data_by_location[entry['locationMainNumber']] = {k: v for k, v in entry.items() if k != 'locationMainNumber'}

    # pprint.pprint(data_by_location)

    total_number_of_plays = int(permit_dict['EndOfDayRapportAntalSpil'])
    total_money_inserted = float(permit_dict['EndOfDayRapportIndskudTotal'])
    total_money_paid_out = float(permit_dict['EndOfDayRapportGevinsterSpil'])
    total_jackpot_money_won = float(permit_dict['EndOfDayRapportGevinsterJackpot'])

    assert total_number_of_plays == sum([v['numberOfPlays'] for _, v in data_by_location.items()]), \
        "Total numberOfPlays is not equal to the sum of locations data"
    assert total_money_inserted == sum([v['moneyInserted'] for _, v in data_by_location.items()]), \
        "Total moneyInserted is not equal to the sum of locations data"
    assert total_money_paid_out == sum([v['moneyPaidOut'] for _, v in data_by_location.items()]), \
        "Total moneyPaidOut is not equal to the sum of locations data"
    assert total_jackpot_money_won == sum([v['jackpotMoneyWon'] for _, v in data_by_location.items()]), \
        "Total jackpotMoneyWon is not equal to the sum of locations data"

    # pprint.pprint(data_by_location)
    return datetime.strptime(permit_dict['EndOfDayRapportDato'], "%Y-%m-%dZ").date(), data_by_location


def parse_safe_file(safe_filename: str):
    with open(safe_filename, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    safe_dict = xmltodict.parse(xml_content)

    # pprint.pprint(safe_dict)

    safe_data = parse_xml_dict(safe_dict)

    # pprint.pprint(safe_data)
    return safe_data

