import asyncio
import aiohttp
from loguru import logger

from navigation import HEADERS, URL


async def _get_postal_codes_from_usps(postal_codes: list[str]):
    '''
        Creates the async session and calls the obtain function
    '''
    async with aiohttp.ClientSession() as session:
        data = await _create_tasks_and_obtain_postal_codes(session, postal_codes)

    return data


async def _create_tasks_and_obtain_postal_codes(session: aiohttp.ClientSession, postal_codes: list[str]):
    '''
        Gathers all the tasks, in this case, requests for get page
    '''
    tasks = [
        asyncio.create_task( _obtain_postal_code_from_usps(session, postal_code) )
        for postal_code in postal_codes
    ]

    results = await asyncio.gather(*tasks)
    return results


async def _obtain_postal_code_from_usps(session: aiohttp.ClientSession, postal_code: str) -> dict:
    '''
        Prepares the body and sends the request
    '''
    logger.debug(f'Sending Request for ZIP: {postal_code}')

    async with session.post(
        url             = URL['CITY_BY_ZIP'], 
        data            = {'zip': postal_code}, 
        headers         = HEADERS, 
        allow_redirects = False
    ) as response:
        logger.debug(f'Processing ZIP: {postal_code}\t|\tStatus Code: {response.status}')
        return {zip: await response.json(content_type=None)}