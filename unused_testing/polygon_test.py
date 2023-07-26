import json
import requests as rq
import pandas as pd
import time

api_url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/3/hour/2021-07-19/2023-07-19?adjusted=true&sort=desc&limit=50000&apiKey=4Eqgqi3RkK6JwXTftEwg_bbp_hMkamaN"

# API call, returns a dictionary "prices"
# prices = rq.get(api_url).json()

# print(pd.DataFrame(prices['results']))


def make_call(url):
    try:
        call = rq.get(url)
        if(call.status_code != 200):
            print(f"API Call failed with status code: {call.status_code}")
        else:
            print(call.json()['results'][-1])
    except rq.exceptions.Exception as err:
        print(err)


while True:
    make_call(api_url)
    time.sleep(20)