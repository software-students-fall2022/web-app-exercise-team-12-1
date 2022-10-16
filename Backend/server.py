import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'shedule',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Events(db.Document):
    name = db.StringField()
    description = db.StringField()
    status = db.StringField()
    time = db.StringField()
    location = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "description": self.description,
                "status": self.status,
                "time": self.time,
                "location": self.location
                }

#show all the events in homepage
@app.route('/', methods=['GET'])
def home_page():
    events = Events.objects()
    render_template("templates/index.html",
        events=events)

#create event
@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    event = Events(name=record['name'],
                description=record['description'],
                status=record['status'],
                time=record['time'],
                location=record['location'])
    event.save()
    return jsonify(event.to_json())

#edit the event
@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    event = Events.objects(name=record['name']).first()
    if not event:
        return jsonify({'error': 'event not found'})
    else:
        event.update(email=record['email'])
    return jsonify(event.to_json())

#delete the event
@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    event = Events.objects(name=record['name']).first()
    if not event:
        return jsonify({'error': 'event not found'})
    else:
        event.delete()
    return jsonify(event.to_json())

#search for the event
@app.route('/search', methods=['GET']) 
def query_records():
    name = request.args.get('name')
    event = Events.objects(name=name).first()
    if not event:
        return jsonify({'error': 'event not found'})
    else:
        return jsonify(event.to_json())

if __name__ == "__main__":
    event = Events(name="123",
                description="123",
                status="123",
                time="123",
                location="123")
    event.save()
    app.run(debug=True)

