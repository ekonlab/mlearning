import gzip
import simplejson as json
import os

files = []
gzips = []

for file in os.listdir('.'):
    if os.path.isfile(file) and os.path.splitext(file)[1][1:] == 'gz':
        gzips.append(file)
        file_data = dict()
        file_name = os.path.splitext(file)[0][1:] + '.json'
        file_data["name"] = file_name
        file_data["body"] = json.load(gzip.open(file))
        files.append(file_data)

for file in os.listdir('.'):
    if os.path.isfile(file) and os.path.splitext(file)[1][1:] == "gz'":
        file_data = dict()
        file_name = os.path.splitext(file)[0][1:] + '.json'
        file_data["name"] = file_name
        file_data["body"] = json.load(gzip.open(file))
        files.append(file_data)

for file in files:
    with open(file["name"],'w') as out:
        json.dump(json.loads(file["body"]),out)

for file in gzips:
    os.remove(file)
