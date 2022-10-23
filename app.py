from asyncio import events
import json
from multiprocessing import Event
from django.shortcuts import render
from flask import Flask, request, redirect, jsonify, render_template, url_for
from bson.json_util import dumps,loads
import pymongo

app = Flask(__name__)
app.static_folder = 'static'
app.config['MONGODB_SETTINGS'] = {
    'db': 'shedule',
    'host': 'localhost',
    'port': 27017
}


# read connection string from env file
# db username,pw remove
myclient = pymongo.MongoClient()
mydb = myclient["shedule"]
mycol = mydb["events"]

#home page
@app.route('/', methods=['GET'])
def home_page():
    events = mycol.find({}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)]).limit(5)
    return render_template("home.html", events=events)


# view upcoming homework
@app.route('/view_homework', methods=['GET'])
def show_homework():
    events = mycol.find({"tag": "homework"}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("homework.html", events=events)


# view upcoming exams
@app.route('/view_exam', methods=['GET'])
def show_exam():
    events = mycol.find({"tag": "exam"}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("exam.html", events=events)


# view upcoming interviews
@app.route('/view_interview', methods=['GET'])
def show_interview():
    events = mycol.find({"tag": "interview"}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("interview.html", events=events)


# view upcoming misc
@app.route('/view_misc', methods=['GET'])
def show_misc():
    events = mycol.find({"tag": "misc"}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("misc.html", events=events)


#view in calendar
@app.route('/calendar_view', methods=['GET'])
def show_calendar():
    events = mycol.find({}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    list_cur = list(events)
    json_data = loads(dumps(list_cur, indent=2))    
    return render_template("calendarView.html",events=json_data)



# add event(get)
@app.route('/add_event', methods=['GET'])
def add_task():
    events = mycol.find({}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("addEvent.html", events=events)


# add event(post)
@app.route('/add_event', methods=['POST'])
def create_record():
    event = {
        "name":  request.form['name'],
        "date": request.form['task-date'],
        "status": "active",
        "time":  request.form['task-time'],
        "tag": request.form['task-tag']
    }
    x = mycol.insert_one(event)
    if not x:
        return jsonify({"message": "Error occured"}), 500
    return redirect(url_for('home_page'))


# edit the event
@ app.route('/update_record/<event_name>', methods=['GET', 'POST'])
def update_record(event_name):
    myquery = {"name": event_name}
    newvalues = {
        "$set": {"date": request.form["task-date"],
                 "status": request.form["status"],
                 "time": request.form["task-time"]
                }
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
    #mycol.delete_many({})
    return redirect(url_for('home_page'))


# search for the event
@ app.route('/search_record', methods=['POST', 'GET'])
def query_records():
    name = request.form["name"]
    myquery = {"name": name}
    events = mycol.find(myquery, projection={"_id": 0})
    if mycol.count_documents(myquery) == 0:
        find = 0
        return render_template("search.html", events=events, find=find)
    else:
        find = 1
        return render_template("search.html", events=events, find=find)


if __name__ == "__main__":
    app.run(debug=True)
