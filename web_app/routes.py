from flask import render_template, send_from_directory
from web_app import app
from hardware_manager import step
from hardware_manager import dht
from hardware_manager import bh1750
import json


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.xhtml', temp_1=dht.DHTSensor.get_instance("indoor").temp,
                           hum_1=dht.DHTSensor.get_instance("indoor").humid)


@app.route('/api/sensors')
def sensors():  # lux.luminance
    dht_1 = dht.DHTSensor.get_instance("indoor")
    lux_1 = bh1750.BH1750.get_instance("indoor")
    lux_2 = bh1750.BH1750.get_instance("outdoor")
    data = {"indoor": {"luminance": lux_1.luminance, "temperature": dht_1.temp, "humidity": dht_1.humid},
            "outdoor": {"luminance": lux_2.luminance, "temperature": 10, "humidity": 44}} # TODO: add real sensor
    return json.dumps(data)


@app.route('/api/stepper/get_status')
def status():
    msg = json.dumps({"status": step.Stepper.get_instance().allowed,
                      "steps": step.Stepper.get_instance().scheduled_steps,
                      "current_position": step.Stepper.get_instance().current_position,
                      "scheduled_position": step.Stepper.get_instance().scheduled_position})
    return msg


@app.route('/api/stepper/set_position/<pos>')
def new_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().scheduled_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().scheduled_position})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})
    return msg



@app.route('/api/stepper/set_steps/<st>')
def set_steps(st):
    try:
        st = int(st)
        step.Stepper.get_instance().scheduled_steps = st
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().scheduled_steps})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})
    return msg


@app.route('/api/stepper/set_current_position/<pos>')
def set_current_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().current_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().current_position})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})
    return msg


@app.route('/api/stepper/set_status/<int:val>')
def set_status(val):
    try:
        step.Stepper.get_instance().allowed = bool(int(val))
    except ValueError:
        pass
    except TypeError:
        pass
    msg = json.dumps({"status": step.Stepper.get_instance().allowed})
    return msg
