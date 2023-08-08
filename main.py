#Initialization
from flask import *
from flask_cors import CORS, cross_origin
import json
import pymongo
import os
import dns

print("working?*")
print("bruh2")


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
  rows = 10
  cols = 10
  data = [[0 for j in range(cols)] for i in range(rows)]

  # Insert the 2D array-like data into MongoDB
  collection.update_one({}, {"$set": {"build1": data}})
  return collection.find({})


def dbUpdateCell(collection, row, column, new_value):
  # Update the cell value in the MongoDB collection
  collection.update_one({}, {"$set": {f"build1.{row}.{column}": new_value}})
  print("dbUpCell", collection.find({})[0])
  return collection.find({})[0]


def dbPrint(collection):
  #print collection[0]
  cursor = collection.find({})
  for document in cursor:
    print(document)


collection = dbConnect()

tables = collection.find({})
for document in tables:
  lastTable = {'table': document['build1']}
  print(lastTable)
  print('****')

# Convert Python dictionary to JSON
json_data = json.dumps(lastTable)
print(json_data)

#--------------------------------------------------------

#os.system('clear')
app = Flask("ZooryDB")
port = 8083
host = "0.0.0.0"

CORS(app)


#home page
@app.route('/')
def index():
  return render_template("index.html")


#send board data out
@app.route('/board', methods=['GET', 'POST'])
def board():
  if request.method == 'POST':
    print("again", json.dumps({'table': collection.find({})[0]['build1']}))
    return json.dumps({'table': collection.find({})[0]['build1']})
  return json.dumps({'table': collection.find({})[0]['build1']})


@app.route('/move', methods=['GET', 'POST'])
def receive_integer():
  if request.method == 'POST':
    try:
      received_data = (request.json)
      print(received_data)
      lastTable = dbUpdateCell(collection, received_data["row"],
                               received_data["column"], received_data["state"])
      json_data = json.dumps({'table': lastTable['build1']})

      return {"msg": "got it"}
    except ValueError:
      return "Invalid input. Please enter a valid integer."
  return "gimme"


#This just sets the required params such as the host to run on and port to run on and if debug is on.
#if __name__ == "__main__":
app.run(host, port, debug=False)
