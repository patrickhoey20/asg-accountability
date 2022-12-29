import csv
import json

rows = None
with open('pivotcsvs/data1920.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    rows = [row for row in reader]
with open('pivotjsons/data1920.json', 'w') as json_file:
    json.dump(rows, json_file)
