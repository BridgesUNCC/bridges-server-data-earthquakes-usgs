from flask import Flask, jsonify
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import simplejson as json
import os
import time
import urllib.request
app = Flask(__name__)
client = None

MLAB_HOST = os.getenv("MLAB_HOST")
MLAB_PORT = os.getenv("MLAB_PORT")
MLAB_PWORD = os.getenv("MLAB_PWORD")
MLAB_USER = os.getenv("MLAB_USER")
MLAB_DB = os.getenv("MLAB_DB") or "eqs"
MLAB_URI = os.getenv("MONGODB_URI")
MLAB_COLLECTION = os.getenv("MLAB_COLLECTION") or "eqs"
EQ_LIMIT = 50_000

_uri = None
if MLAB_URI is not None:
    _uri = MLAB_URI
elif MLAB_USER is not None and MLAB_PWORD is not None and MLAB_PWORD is not None and MLAB_USER is not None:
    _uri = f"mongodb://{MLAB_USER}:{MLAB_PWORD}@{MLAB_HOST}:{MLAB_PORT}/"

if _uri is not None:
    client = MongoClient(_uri)
else:
    client = MongoClient()

db = client[MLAB_DB]
collection = db[MLAB_COLLECTION]


@app.route('/')
def landing_page():
    return 'useful information goes here'


@app.route('/eq/latest/<int:number>')
def latest_eq(number):
    return jsonify(Earthquakes=json.loads(dumps(collection.find().sort({time: pymongo.ASCENDING}).limit(int(number)))))


@app.route('/eq')
def all_eq():
    return jsonify(Earthquakes=json.loads(dumps(collection.find())))


def fetch_eqs():
    print(str(time.time()) + " EQ FETCH")
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson"
    with urllib.request.urlopen(url) as json_data:
        data = json.loads(json_data.read().decode())
        db_ids = [item["id"] for item in list(collection.find({}, ['id'])) if "id" in item.keys()]
        to_insert = []
        for item in data["features"]:
            if item['id'] not in db_ids:
                props = item["properties"]
                geom = item["geometry"]
                eq = {
                    "id": item['id'],
                    "properties": {
                        "mag": props["mag"],
                        "place": props["place"],
                        "title": props["title"],
                        "url": props["url"],
                        "time": props["time"]
                    },
                    "geometry": {
                        "coordinates": geom["coordinates"]
                    }
                }
                to_insert.append(eq)
        print(str(len(to_insert)) + " to insert")
        if len(to_insert) != 0:
            if len(db_ids) >= EQ_LIMIT:
                to_del = [item["id"] for item in list(collection.find({}, ['id'])
                                                      .sort({time: pymongo.DESCENDING}).limit(len(to_insert)))
                          if "id" in item.keys()]
                for i in to_del:
                    collection.remove({"id": i})

            collection.insert(to_insert)


def ping():
    site_url = "https://earthquakes-uncc-yes.herokuapp.com"
    print(urllib.request.urlopen(site_url))


@app.before_first_request
def init():
    fetch_eqs()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_eqs, trigger="interval", minutes=25)
    scheduler.add_job(func=ping, trigger="interval", minutes=25)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
