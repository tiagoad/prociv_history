import requests
import json
import os

# config - all in ms
START = 1553623452804
END = 1555434252804
INTERVAL = 604800000 - 3600000 # daylight saving...

# constants
URL = "http://www.prociv.pt/_vti_bin/ARM.ANPC.UI/ANPC_SituacaoOperacional.svc/GetHistoryOccurrencesSearchRange"
JSON_DIR = "json"

def get_page(start_timestamp, end_timestamp, page=1, size=1):
    r = requests.post(URL, 
        json=dict(
            dataFechoOperacional=f"/Date({end_timestamp}+0000)/",
            dataOcorrencia= f"/Date({start_timestamp}+0000)/",
            distritoID=None,
            naturezaID=None,
            pageIndex=page,
            pageSize=size),
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                'referer': URL
            })
        
    return r.json()

def flatten_dict(d):
    out = {}

    for k, v in d.items():
        if type(v) == dict:
            for ik, iv in flatten_dict(v).items():
                out[f'{k}.{ik}'] = iv
        
        else:
            out[k] = v

    return out

def get_interval_data(start_timestamp, end_timestamp):
    # one record to get total
    data = get_page(start_timestamp, end_timestamp, 1, 1)
    total = data['GetHistoryOccurrencesSearchRangeResult']['arrayInfo'][0]['Total']

    print(f'Getting {total} records')

    # all the data
    data = get_page(start_timestamp, end_timestamp, 1, total)
    records = data['GetHistoryOccurrencesSearchRangeResult']['arrayInfo'][0]['Data']

    return list(map(flatten_dict, records))

remaining = (END-START)//INTERVAL

# ensure directory exists
os.makedirs(JSON_DIR, exist_ok=True)

# scrape json
timestamp = START
while True:
    print(f'{remaining} downloads remaining.')

    fr = timestamp
    to = timestamp + INTERVAL
    print(f'{fr} -> {to}')

    data = get_interval_data(fr, to)

    print(f'Got {len(data)} records')

    with open(f'{JSON_DIR}/{fr}_{to}.json', 'w') as f:
        f.write(json.dumps(data))

    if to > END:
        break

    timestamp += INTERVAL
    remaining -= 1
