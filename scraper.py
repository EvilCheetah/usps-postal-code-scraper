import json
from os import getenv
import aiohttp
import asyncio
from pathlib import Path
from datetime import (datetime, timedelta)

from request import _get_postal_codes_from_usps



def get_postal_codes():
    '''
        Returns one of the following options:
            - If there exists a cached data, return it
            - If not, obtain from USPS

    '''
    if ( 
        _file_is_fresh( Path(getenv('OUTPUT_DIRECTORY')) / Path(getenv('OUTPUT_FILE')) )
    ):
        return json.load(
            Path(getenv('OUTPUT_DIRECTORY')) / Path(getenv('OUTPUT_FILE'))
        )

    return _prepare_postal_codes_and_obtain()


def _file_is_fresh(file_in: Path):
    '''
        Checks if file exists and it is not outdated
        
    '''
    return (
        ( file_in.is_file() ) and
        ( timedelta(hours = 12) > ( datetime.now() - datetime.fromtimestamp(file_in.stat().st_mtime)) )
    )


def _prepare_postal_codes_and_obtain():
    '''
        Populates a list of all possible postal-codes
    '''
    # Populate a list of postal codes
    postal_codes = [f'{postal_code:05d}' for postal_code in range(100_000)]
    data         = asyncio.run( _get_postal_codes_from_usps(postal_codes) )

    # Chache the file
    with open('data.json', 'w') as fout:
        json.dump(data, fout, indent = 4)

    return data
