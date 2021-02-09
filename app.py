from flask import Flask, render_template, request, redirect, url_for, jsonify, json, make_response
from flask_sqlalchemy import SQLAlchemy
import requests
import urllib3
from qhue import Bridge
from torrent import find_torrent_list
# from hub import sensor_read
from sqlalchemy.inspection import inspect
import datetime

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:///sensors'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    @staticmethod
    def serlialize_list(l):
        return [m.serialize() for m in l]

class Sensors_db(db.Model, Serializer):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    pressure = db.Column(db.Integer, nullable=False)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def __repr__(self):
        return f'<Reading {self.id} | pressure {self.pressure}>'
db.create_all()

bridge_username = 'bzyWKfvOkgNqFtRahH01WYX8efdA1kBRqUMPF1Nq'
Bridge_IP = '192.168.1.30'

def lights_now():
    try:
        b = Bridge(Bridge_IP, bridge_username)
        lights_now = b.lights[1]()['state']['on']
        status = 'on' if lights_now else 'off'
        elec = "Power"
        return b, status, elec
    except:
        status = 'off'
        elec = "No Power"
        return b, status, elec

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            b, status, elec = lights_now()
            value = request.form['brightness']
            b.lights[1].state(on= True, bri=int(value))
            percentage = f'{int((int(value) / 254) * 100)}%'
            return render_template('index.html', **locals())
        else:
            percentage = '50%'
            b, status, elec = lights_now()
            return render_template('index.html', **locals())
    except requests.exceptions.ConnectionError:
        elec = "No Power"
        return render_template('index.html', **locals())

@app.route('/on', methods=['GET', 'POST'])
def lights_on():
    try:
        b, status, elec = lights_now()
        b.lights[1].state(on= True, bri=100)
        return redirect(url_for('index'))
    except requests.exceptions.ConnectionError:
        return redirect(url_for('index'))

@app.route('/off')
def lights_off():
    try:
        b, status, elec = lights_now()
        b.lights[1].state(on= False)
        return redirect(url_for('index'))
    except requests.exceptions.ConnectionError:
        return redirect(url_for('index'))

@app.route('/torrent', methods=['GET', 'POST'])
def torrent():
    if request.method == 'POST':
        search_string = request.form['search']
        search_string.replace(' ', '%20')
        list_of_titles, list_of_magnets, list_of_sizes, list_of_timestamps = find_torrent_list(search_string)
        if list_of_titles == []:
            return render_template('torrent.html', **locals())
        else:
            titles = lambda: zip(list_of_titles, list_of_magnets, list_of_sizes, list_of_timestamps)
            return render_template('torrent_result.html', **locals())
    else:
        return render_template('torrent.html')

@app.route('/torrent_result', methods=['GET', 'POST'])
def torrent_result():
    if request.method == 'POST':
        search_string = request.form['search']
        search_string.replace(' ', '%20')
        list_of_titles, list_of_magnets, list_of_sizes, list_of_timestamps = find_torrent_list(search_string)
        if list_of_titles == []:
            return render_template('torrent_result.html', **locals())
        else:
            titles = lambda: zip(list_of_titles, list_of_magnets, list_of_sizes, list_of_timestamps)
            return render_template('torrent_result.html', **locals())
    else:
        return render_template('torrent_result.html')

@app.route('/sensors')
def sensors():
    # readings = sensor_read()
    return render_template('sensors.html', **locals())

@app.route('/sensor_update', methods=['POST'])
def sensor_update():
    req = request.get_json()
    print(req)
    days = req['days']
    hours = req['hours']
    minutes = req['minutes']
    interval = datetime.datetime.now() - datetime.timedelta(days=days, hours=hours, minutes=minutes)

    data = Sensors_db.query.filter(Sensors_db.timestamp > interval)

    response = make_response()
    response.data = json.dumps(Sensors_db.serlialize_list(data))


    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)