import xmltodict
import pprint
from datetime import datetime, date


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

    ret_dict = {
        'totalNumberOfPlays': int(permit_dict['EndOfDayRapportAntalSpil']),
        'date': datetime.strptime(permit_dict['EndOfDayRapportDato'], "%Y-%m-%dZ").date(),
        'totalMoneyInserted': float(permit_dict['EndOfDayRapportIndskudTotal']),
        'totalMoneyPaidOut': float(permit_dict['EndOfDayRapportGevinsterSpil']),
        'totalJackpotMoneyWon': float(permit_dict['EndOfDayRapportGevinsterJackpot']),

        'locations': get_locations_info(data_dict['SpecifiktSpilstedListe']['SpecifiktSpilsted'])
    }

    # pprint.pprint(ret_dict)
    return ret_dict


def parse_safe_file(safe_filename: str):
    with open(safe_filename, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    safe_dict = xmltodict.parse(xml_content)

    # pprint.pprint(safe_dict)

    safe_data = parse_xml_dict(safe_dict)

    # pprint.pprint(safe_data)
    return safe_data

