urls = ['https://google.com',
'https://www.nytimes.com/guides/',
'https://www.mediamatters.org/',
'https://1.1.1.1/','https://www.apple.com/',
'https://regex101.com/',
'https://docs.python.org/3/this-url-will-404.html',
'https://www.politico.com/tipsheets/morning-money',
'https://www.bloomberg.com/markets/economics',
'https://www.ietf.org/rfc/rfc2616.txt']


import aiohttp
import asyncio
from aiohttp import ClientSession
MAX_REQS_PER_SITE = 100

response_results = {}.fromkeys(urls)

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.
    kwargs are passed to `session.request()`.
    """
    try:
        resp = await session.request(method="GET", url=url, timeout=2, **kwargs)
    except:
        resp = type('obj', (object,), {'status' : 'timed_out!'})
    if response_results[url] is None:
        response_results[url] = {}
    if resp.status not in response_results[url].keys():
        response_results[url][resp.status] = 0
    response_results[url][resp.status] += 1
    print("Got response [{}] for URL: {}".format(resp.status, url),response_results[url])
    return resp.status #html


async def bulk_crawl(urls: set, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            for i in range(MAX_REQS_PER_SITE):
                tasks.append(fetch_html(url=url, session=session, **kwargs))
        await asyncio.gather(*tasks)

asyncio.run(bulk_crawl(urls=urls))

for url in response_results:
    print(url, response_results[url])
