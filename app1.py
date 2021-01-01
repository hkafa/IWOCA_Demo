from flask import Flask, render_template, request
import requests
from qhue import Bridge

app = Flask(__name__)

bridge_username = 'bzyWKfvOkgNqFtRahH01WYX8efdA1kBRqUMPF1Nq'

def lights_now():
    b = Bridge('192.168.1.3', bridge_username)
    lights_now = b.lights[1]()['state']['on']
    status = 'on' if lights_now else 'off'
    return status

@app.route('/',methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            value = request.form['brightness']
            b = Bridge('192.168.1.3', bridge_username)
            b.lights[1].state(on= True, bri=int(value))
            status = lights_now()
            return render_template('index.html', **locals())
        else:
            status = lights_now()
            return render_template('index.html', **locals())
    except requests.exceptions.ConnectionError:
        return render_template('Error.html')

@app.route('/on', methods=['GET', 'POST'])
def lights_on():
    b = Bridge('192.168.1.3', bridge_username)
    b.lights[1].state(on= True, bri=100)
    status = lights_now()
    return render_template('index.html', **locals())

@app.route('/off')
def lights_off():
    b = Bridge('192.168.1.3', bridge_username)
    b.lights[1].state(on= False)
    status = lights_now()
    return render_template('index.html', **locals())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


