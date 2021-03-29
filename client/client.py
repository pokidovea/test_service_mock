from time import sleep

import requests

for i in range(10):
    try:
        response = requests.get('http://google.com:1090/simpleFirst')
    except Exception as e:
        print(str(e))
        sleep(10)
        continue

    if response.status_code != 200:
        print(response.status_code)
        sleep(10)
    else:
        print(response.content.decode('utf-8'))
        break
