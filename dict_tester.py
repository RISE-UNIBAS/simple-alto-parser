import json

# open json file and load it
json_file = 'assets/dicts/locations.json'
with open(json_file) as f:
    data = json.load(f)

ids = []
for loc in data:
    if loc["geonames_id"] not in ids:
        ids.append(loc["geonames_id"])
    else:
        print("Already in list:", loc["geonames_id"], loc["entry"])

