import json
from flask import Flask, request, redirect, jsonify, render_template, url_for
import pymongo


app = Flask(__name__)
app.static_folder = 'static'
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
    return render_template("index.html", events=events)


# create event
@app.route('/', methods=['POST'])
def create_record():
    # record = json.loads(request.data)
    event = {
        "name":  request.form['name'],
        "date":  request.form['task-date'],
        "status": "active",
        "time":  request.form['task-time']
    }
    mycol.insert_one(event)
    return redirect(url_for('home_page'))


# edit the event
@ app.route('/update_record/<event_name>', methods=['POST'])
def update_record(event_name):
    record = json.loads(request.data)
    myquery = {"name": event_name}
    newvalues = {
        "$set": {"date": record["date"],
                 "status": record["status"],
                 "time": record["time"]}
    }
    event = mycol.update_one(myquery, newvalues)
    if not event:
        return jsonify({'error': 'event not found'})
    return redirect(url_for('home_page'))


# delete the event
@ app.route('/delete_record/<event_name>', methods=['GET', 'POST'])
def delete_record(event_name):
    event = mycol.delete_one({"name": event_name})
    if not event:
        return jsonify({'error': 'event not found'})
    return redirect(url_for('home_page'))


# delete all the events (for testing purpose)
@ app.route('/clear')
def delete_all():
    mycol.delete_many({})
    return redirect(url_for('home_page'))


# search for the event
@ app.route('/search', methods=['GET'])
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
