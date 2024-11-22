from flask import Flask, jsonify, render_template
from api.data_manager import init_db, Aircraft, start_background_fetch
import folium

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
    
@app.route('/')
def map_view():
    map_center = [41.1579, -8.629]  #Porto, Portugal
    m = folium.Map(location=map_center, zoom_start=7)

    map_html = m._repr_html_()

    return render_template('map.html', map_html=map_html)

if __name__ == '__main__':
    start_background_fetch(app)

    app.run(debug=True)
