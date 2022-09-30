'''
    Author: Eugene Moshchyn
    Description:
        This program scrapes all ZIP codes from
        USPS Website
'''

import json
import asyncio
import aiohttp
from pathlib import Path
from datetime import (datetime, timedelta)
from navigation import (URL, HEADERS)
import format


async def get_page(session, zip):
    '''
        Gets the page information, keeping the logging
    '''
    data = {'zip': zip}
    print(f'Sending Request for ZIP: {zip}')

    async with session.post(URL['CITY_BY_ZIP'], data = data, headers = HEADERS, allow_redirects = False) as response:
        print(f'Processing ZIP: {zip} --- Status Code: {response.status}')
        return {zip: await response.json(content_type=None)}


async def get_all_pages(session, zips):
    '''
        Gathers all the tasks
    '''
    tasks = [
        asyncio.create_task( get_page(session, zip) )
        for zip in zips
    ]

    results = await asyncio.gather(*tasks)
    return results


async def response(zips):
    '''
        Creates the async session
    '''
    async with aiohttp.ClientSession() as session:
        data = await get_all_pages(session, zips)

    return data


def _get_zip_code_data():
    # Run all 5 digit ZIP codes
    zip_list = [f'{zip:05d}' for zip in range(100_000)]
    data = asyncio.run( response(zip_list) )

    # Chache the file
    with open('data.json', 'w') as fout:
        json.dump(data, fout, indent = 4)

    return format.format_json( Path('data.json') )


def _file_is_good(file_in: Path):
    return (
        ( file_in.is_file() ) and
        ( timedelta(hours = 12) > ( datetime.now() - datetime.fromtimestamp(file_in.stat().st_mtime)) )
    )


def get_data():
    fin = Path('formatted.json')
    if ( _file_is_good(fin) ):
        return json.load( fin.open('r') )

    fin = Path('data.json')
    if ( _file_is_good(fin) ):
        return format.format_json(fin)

    return _get_zip_code_data()


def main():
    # Format of ZIP codes: XXYYY => Total Number = 100,000
    data = get_data()

    for city, zip in data.items():
        print(f'{city} - {zip}')

    print()
    print(f'First ZIP: {list(data.values())[0]}')
    print(f'Last  ZIP: {list(data.values())[-1]}')
    print(f'Total Num of ZIPs: {len(data.keys())}')

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Program was terminated...")
