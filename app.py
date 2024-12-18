from flask import Flask
from bson import json_util, ObjectId
from pymongo import MongoClient
import json


MONGODB_URI = "mongodb://devops:redpanda@127.0.0.1"

client = MongoClient(MONGODB_URI)

db = client.mydata
coll = db.data
app = Flask(__name__)


@app.route('/add/<species>/<bird>')
def add(species, bird):
    new_bird = {"species": str(species), "bird":  str(bird)}
    x = coll.insert_one(new_bird)
    print(x.inserted_id)
    return str(x.inserted_id)

@app.route('/all')
def get_all():
  birds = []
  cursor = coll.find({}, {"_id": 1, "bird": 1})
  for document in cursor:
    birds.append(document) 
  page_sanitized = json.loads(json_util.dumps(birds))
  print(birds)
  return page_sanitized

@app.route('/del/<id>')
def delete_bird(id):
  delete_bird = {'_id': ObjectId(str(id))}
  y = coll.delete_one(delete_bird)
  print(y.deleted_count)
  return str(y.deleted_count)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
