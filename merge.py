import json
import glob
import csv

JSON_DIR = "json"

full = []

for fn in glob.glob('json/*.json'):
    print(fn)

    with open(fn) as f:
        raw = f.read()
        data = json.loads(raw)
        full += data


with open('out.csv', 'w') as f:
    allkeys = set()

    # find all possible keys
    for record in full:
        allkeys.update(record.keys())

    writer = csv.DictWriter(f, fieldnames=allkeys)
    writer.writeheader()

    for record in full:
        writer.writerow(record)
