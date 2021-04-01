from time import sleep

import requests

URLS = [
    'http://facebook.com/',
    'http://facebook.com/hi/',
    'http://facebook.com/hello/',
]

for url in URLS:
    for i in range(10):
        try:
            response = requests.get(url)
        except Exception as e:
            print(str(e))
            sleep(10)
            continue

        print(response.content.decode('utf-8'))
        break
