'''
    Author: Eugene Moshchyn
    Description:
        This file is designated to format and sort received data
'''
import json
from pathlib import Path
from collections import defaultdict


def format_json(fin: Path) -> None:
    data = json.load(fin.open('r'))

    zip_city = defaultdict( list )

    # Loops over the JSON and records the existing ZIPs
    for entry in data:
        for (zip, result) in entry.items():
            if (result['resultStatus'] == 'SUCCESS'):
                city_state = f'{result.get("defaultCity",  "N/A")}, {result.get("defaultState", "N/A")}'
                zip_city[city_state].append(zip)

    # Sorts JSON by ZIP
    city_zip = {
        zip: location
        for (zip, location)
        in sorted(zip_city.items(), key = lambda item: item[0])
    }

    json.dump(city_zip, Path('formatted.json').open('w'), indent = 4)

    return zip_city


def main():
    fin = Path('data.json')

    if ( not fin.is_file() ):
        raise Exception('File `data.json` does not exist')

    format_json(fin)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('Program was terminated')
