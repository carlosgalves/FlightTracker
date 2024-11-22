import requests
import time
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

FETCH_INTERVAL = 5 #segundos

db = SQLAlchemy()

class Aircraft(db.Model):
    hex = db.Column(db.String(10), primary_key=True)
    flight = db.Column(db.String(10), nullable=True)
    squawk = db.Column(db.String(4), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.String(4), nullable=True)
    ground_speed = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Aircraft {self.hex}>"


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def fetch_and_save_aircraft():
    url = 'https://ads-b.tail76af06.ts.net/data/aircraft.json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with current_app.app_context():
            Aircraft.query.delete()

            for aircraft in data.get('aircraft', []):
                new_aircraft = Aircraft(
                    hex=aircraft.get('hex'),
                    flight=aircraft.get('flight'),
                    latitude=aircraft.get('lat'),
                    longitude=aircraft.get('lon'),
                    altitude=aircraft.get('alt_baro', 'N/A'),
                    ground_speed=aircraft.get('gs'),
                    squawk=aircraft.get('squawk')
                )
                db.session.add(new_aircraft)

            db.session.commit()

        print("Aircraft data saved successfully!")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the data: {e}")

def periodic_fetch(interval_seconds, app):
    with app.app_context():
        while True:
            fetch_and_save_aircraft()
            time.sleep(interval_seconds)

def start_background_fetch(app):
    fetch_thread = Thread(target=periodic_fetch, args=(FETCH_INTERVAL, app))
    fetch_thread.daemon = True
    fetch_thread.start()
