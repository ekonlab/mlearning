import os
import simplejson as json
from pymongo import MongoClient
import time
import geojson
from collections import defaultdict


def load_files(files,counter):
  i = 0
  data = []
  geodata = []
  for file_name in files[:5]:
    i += 1
    counter["index"] += 1
    fl = open(file_name)
    data += [delete_old_ids(d) for d in json.load(fl)]
    #geodata += [json2geojson(data, file_name)]
    print('loading file: ' + file_name + ' - ' + str(counter["index"]) + '/' + str(counter["len"]));
    fl.close()
  
  files = files[5:]
  return data, files
  

def setup_db_connection():
  client = MongoClient()
  db = client.flights_db
  coll = db.all_points
  geocoll = db.geo_lines
  
  return coll, geocoll


def bulk_data(coll, data):
  for doc in data:
    coll.insert_one(doc)
  

def json2geojson(data, file_name):
  adshex_count = defaultdict(list)
  geodata = geojson.FeatureCollection([])
  
  for doc in data:
    adshex_count[doc["adshex"]].append(doc)
    
  for key in adshex_count.keys():
    line_points = []
    for d in adshex_count[key]:
      if "lat" in d.keys() and "lng" in d.keys():
        line_points.append([d[u"lat"],d[u"lng"]])
    
    geodata["features"].append(geojson.Feature(geometry=geojson.LineString(line_points), properties=adshex_count[key]))
    
  return geodata
    

def delete_old_ids(d):
  del d["_id"]
  return d 


def json2mongo():
  files = os.listdir()
  coll, geocoll = setup_db_connection()
  counter = {
    "index": 0,
    "len": len(files)
  }
  while len(files):
    data, files = load_files(files,counter)
    bulk_data(coll, data)
    #bulk_data(geocoll, geodata)
    time.sleep(10)
    
    
if __name__ == '__main__':
  json2mongo()
  
