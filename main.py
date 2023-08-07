#Initialization
from flask import *
from flask_cors import CORS, cross_origin
import json
import pymongo
import os
import dns

print("working?")


def dbConnect():
  #mongoDB Connection svr url
  token = os.getenv("db-url")
  try:
    client = pymongo.MongoClient(token)
  # return a friendly error if a URI error is thrown
  except pymongo.errors.ConfigurationError:
    print(
      "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
    )
    sys.exit(1)

  #connect to db
  db = client.board
  #connect to collection
  collection = db["tiles"]

  return collection


def dbUpdate(collection):
  # Sample 2D array-like data
  rows = 4
  cols = 5
  data = [[1 for j in range(cols)] for i in range(rows)]

  # Insert the 2D array-like data into MongoDB
  collection.update_one({}, {"$set": {"build1": data}})
  return collection.find({})


def dbPrint(collection):
  #print collection[0]
  cursor = collection.find({})
  for document in cursor:
    print(document)


collection = dbConnect()
tables = dbUpdate(collection)
for document in tables:
  lastTable = {'table': document['build1']}
  print(lastTable)
  print('****')

print(type(lastTable))
print(lastTable)
# Convert Python dictionary to JSON
json_data = json.dumps(lastTable)
print(json_data)

#--------------------------------------------------------

#os.system('clear')
app = Flask("ZooryDB")
port = 8083
host = "0.0.0.0"

CORS(app)


@app.route('/')
def index():
  return render_template("index.html")


@app.route('/data', methods=['GET'])
def data():
  return json_data


#This just sets the required params such as the host to run on and port to run on and if debug is on.
#if __name__ == "__main__":
app.run(host, port, debug=False)
