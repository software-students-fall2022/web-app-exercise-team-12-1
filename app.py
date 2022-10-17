import json
from flask import Flask, request, jsonify, render_template
import pymongo

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'shedule',
    'host': 'localhost',
    'port': 27017
}

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shedule"]
mycol = mydb["events"]


# show all the events in homepage
@app.route('/', methods=['GET'])
def home_page():
    events = mycol.find({}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("index.html",
                           events=events)

# create event


@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    event = {
        "name": record['name'],
        "date": record['date'],
        "status": record["status"],
        "time": record["time"],
        "description": record["description"]
    }
    x = mycol.insert_one(event)
    return jsonify(x)

# edit the event


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    myquery = {"name": record['name']}
    newvalues = {
        "$set": {"date": record['date'],
                 "status": record["status"],
                 "time": record["time"],
                 "description": record["description"]}
    }
    event = mycol.update_one(myquery, newvalues)
    if not event:
        return jsonify({'error': 'event not found'})
    return jsonify(event)

# delete the event


@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    myquery = {"name": record['name']}
    event = mycol.delete_one(myquery)
    if not event:
        return jsonify({'error': 'event not found'})
    return jsonify(event)

# search for the event


@app.route('/search', methods=['GET'])
def query_records():
    name = request.args.get('name')
    myquery = {"name": name}
    events = mycol.find(myquery, projection={"_id": 0})
    if not events:
        return jsonify({'error': 'event not found'})
    else:
        return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
