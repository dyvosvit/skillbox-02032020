'''
ДЗ № 1
Сделать list из списка URL адресов (минимум 5).
Написать цикл, который пробежит по списку URL
и обратиться к каждому N раз (минимум 100) с помощью
библиотеки recuests.
Скинуть код и описать наблюдаемые явления.
'''


import concurrent.futures
import time

urls = ['https://google.com',
'https://www.mediamatters.org/',
'https://www.nytimes.com/guides/',
'https://1.1.1.1/','https://www.apple.com/',
'https://www.bloomberg.com/markets/economics',
'https://regex101.com/',
'https://docs.python.org/3/this-url-will-404.html',
'https://www.politico.com/tipsheets/morning-money',
'https://www.ietf.org/rfc/rfc2616.txt']


import requests
import threading
MAX_REQS_PER_SITE = 100

response_results = {}.fromkeys(urls)

def worker_fetch(url, **kwargs):
    _id = urls.index(url)
    start = time.time()
    with requests.Session() as session:
        for i in range(MAX_REQS_PER_SITE):
            try:
                resp = session.request(method="GET", url=url, timeout=2, **kwargs)
            except:
                resp = type('obj', (object,), {'status_code' : 'timed_out!'})
            if response_results[url] is None:
                response_results[url] = {}
            if resp.status_code not in response_results[url].keys():
                response_results[url][resp.status_code] = 0
            response_results[url][resp.status_code] += 1
            print("[Thread {}] Response [{}] for URL: {}".format(_id, resp.status_code, url),response_results[url])
    response_results[url]['run_time'] = time.time()-start
    print("[Thread {}] for URL: {} - FINISHED in {} seconds!".format(_id, url, time.time()-start),response_results[url])

with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
    executor.map(worker_fetch, urls)

for url in response_results:
    print(url, response_results[url])


