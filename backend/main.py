import aiohttp
import asyncio
import xmltodict
import json

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/07/2001&date_req2=13/07/2001') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html)
            print(json.dumps(xmltodict.parse(html),indent=4))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())