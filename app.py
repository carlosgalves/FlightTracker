from flask import Flask, jsonify
from api.data_manager import init_db, Aircraft, start_background_fetch

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aircraft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

@app.route('/data', methods=['GET'])
def get_aircraft():
    with app.app_context():
        aircrafts = Aircraft.query.all()
    return jsonify([{
        "hex": a.hex,
        "flight": a.flight,
        "squawk": a.squawk,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "altitude": a.altitude,
        "ground_speed": a.ground_speed
    } for a in aircrafts])

if __name__ == '__main__':
    start_background_fetch(app)

    app.run(debug=True)
