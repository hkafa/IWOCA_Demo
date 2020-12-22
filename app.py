from flask import Flask, render_template, request
from qhue import Bridge

app = Flask(__name__)

bridge_username = 'bzyWKfvOkgNqFtRahH01WYX8efdA1kBRqUMPF1Nq'

@app.route('/')
def index():
    df = pd.read_csv('/tmp/pycharm_project_586/ML 325 to predict.csv')
    return render_template('index.html')

@app.route('/on', methods=['GET', 'POST'])
def lights_on():
    b = Bridge('192.168.1.7', bridge_username)
    b.lights[1].state(on= True, bri=150)
    return render_template('index.html')

@app.route('/off')
def lights_off():
    b = Bridge('192.168.1.7', bridge_username)
    b.lights[1].state(on= False, bri=50)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


