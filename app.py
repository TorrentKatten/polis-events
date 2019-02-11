import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from police_api.api import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://police-events:password@localhost/police_events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class PoliceEvent(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.Date, nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(150), nullable=False)
    type = db.Column(UUID(as_uuid=True), db.ForeignKey('type.id'), nullable=False)
    location = db.Column(UUID(as_uuid=True), db.ForeignKey('location.id'), nullable=False)


class Location(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gps = db.Column(db.String(120), unique=True, nullable=False)


class Type(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

db.create_all()

@app.route('/')
def hello_world():
    events = Api.load_recent_events()

    for event in events:
        e = PoliceEvent()
        e.uuid = uuid.uuid4()
        e.datetime = event.datetime
        e.summary = event.summary
        e.name = event.name
        e.id = event.id
        e.url = event.url

        type = Type.query.filter_by(name=event.type).first()

        if type is not None:
            e.type = type.id
        else:
            t = Type()
            t.id = uuid.uuid4()
            t.name = event.type
            e.type = t.id
            db.session.add(t)
            db.session.commit()

        loc = Location.query.filter_by(name=event.location.name, gps=event.location.gps).first()

        if loc is not None:
            e.location = loc.id
        else:
            l = Location()
            l.id = uuid.uuid4()
            l.name = event.location.name
            l.gps = event.location.gps
            e.location = l.id
            db.session.add(l)
            db.session.commit()
        db.session.add(e)
    db.session.commit()

    return 'Events written to DB'

if __name__ == '__main__':

    app.run()
