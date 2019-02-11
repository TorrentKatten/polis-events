import app

def get_events(db): # not  done yet
    return "Number of events: " + str(db.session.query(app.PoliceEvent).with_entities(
        app.PoliceEvent.name,
        app.PoliceEvent.datetime,
        app.PoliceEvent.location
    ).all())
