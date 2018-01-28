import requests
def buildParams(bounds):
    params = {
     "adsb": 1,
    "bounds": buildBounds(bounds),
    "estimated": 1,
    "faa": 1,
    "flarm": 1,
    "gliders": 1,
    "maxage": 14400,
    "mlat": 1,
    "stats": 1,
    "vehicles": 1
    }
    queryParams = '&'.join([( k + '=' + str(v)) for k,v in params.items()])
    return '?' + queryParams
def buildBounds(bounds):
    return ','.join([str(d) for d in bounds])
base_url = "https://data-live.flightradar24.com"
api_route = "/zones/fcgi/feed.js"
template_params = {
"bounds": ["y1","y2","x1","x2"],
"adsb": 1,
"air": 1,
"estimated": 1,
"faa": 1,
"flarm": 1,
"gliders": 1,
"maxage": 14400,
"mlat": 1,
"stats": 1
"vehicles": 1
}
template_params = {
"bounds": ["y1","y2","x1","x2"],
"adsb": 1,
"air": 1,
"estimated": 1,
"faa": 1,
"flarm": 1,
"gliders": 1,
"maxage": 14400,
"mlat": 1,
"stats": 1,
"vehicles": 1
}
%history
%history -o api.py
import os
os.listdir('.')
%history -f flights_api.py
