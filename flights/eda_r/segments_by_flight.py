import os
import pandas as pd
import ijson

os.chdir("/Users/albertogonzalez/Downloads")
cwd = os.getcwd()
print cwd


# Read json with flights
#df = pd.read_json("suspects.json",lines=True)


filename = "suspects.json"
with open(filename, 'r') as f:
    objects = ijson.items(f, 'meta.view.columns.item')
    columns = list(objects)


