from flask import render_template, url_for, flash, redirect, request, abort, send_from_directory
from web_app import app
import hardware_manager.step as step
import hardware_manager.dht as dht

import json

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('static/images', path)

@app.route('/api/get_status')
def status():
    msg = json.dumps({"status": step.Stepper.get_instance().allowed, 
    "steps": step.Stepper.get_instance().steps})
    return msg

@app.route('/api/set_steps/<int:st>')
def move(st):
    try:
        st = int(st)
        step.Stepper.get_instance().steps = st
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().steps})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})
    return msg

@app.route('/api/sensors')
def sensors():#lux.luminance
    dht_instance = dht.DHSensor.get_instance()
    msg = json.dumps({"lux1": 123, "temp1": dht_instance.temp, "hum1": dht_instance.humid})
    return msg

@app.route('/api/set_status/<int:val>')
def set_status(val):
    try:        
        step.Stepper.get_instance().allowed = bool(int(val))
    except ValueError:
        pass
    except TypeError:
        pass
    msg = json.dumps({"status": step.Stepper.get_instance().allowed})
    return msg

