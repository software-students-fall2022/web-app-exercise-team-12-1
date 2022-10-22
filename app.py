from asyncio import events
import json
from django.shortcuts import render
from flask import Flask, request, redirect, jsonify, render_template, url_for
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

# view options/home page


@app.route('/', methods=['GET'])
def home_page():
    return render_template("home.html")

# view upcoming homework


@app.route('/view_homework', methods=['GET'])
def show_homework():
    return render_template("homework.html")

# view upcoming exams


@app.route('/view_exam', methods=['GET'])
def show_exam():
    return render_template("exam.html")

# view upcoming interviews


@app.route('/view_interview', methods=['GET'])
def show_interview():
    return render_template("interview.html")

# view upcoming misc


@app.route('/view_misc', methods=['GET'])
def show_misc():
    return render_template("misc.html")

#view in calendar


@app.route('/calendar_view', methods=['GET'])
def show_calendar():
    return render_template("calendarView.html")

# add event(get)


@app.route('/add_event', methods=['GET'])
def add_task():
    events = mycol.find({}, projection={"_id": 0}).sort(
        [("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)])
    return render_template("addevent.html", events=events)

# add event(post)


@app.route('/add_event', methods=['POST'])
def create_record():
    event = {
        "name":  request.form['name'],
        "date":  request.form['task-date'],
        "status": "active",
        "time":  request.form['task-time'],
        "tag": request.form['task-tag']
    }
    x = mycol.insert_one(event)
    if not x:
        return jsonify({"message": "Error occured"}), 500
    return redirect(url_for('home_page'))

# edit the event


@ app.route('/update_record/<event_name>', methods=['POST'])
def update_record(event_name):
    myquery = {"name": event_name}
    newvalues = {
        "$set": {"date": request.form["task-date"],
                 "status": request.form["status"],
                 "time": request.form["task-time"]}
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
