from flask import render_template, send_from_directory
from web_app import app
from hardware_manager import step
from hardware_manager import dht
from hardware_manager import bh1750
import json
import random

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.xhtml', temp_1=dht.DHTSensor.get_instance("indoor").temp,
                           hum_1=dht.DHTSensor.get_instance("indoor").humid)



@app.route('/api/sensors')
def sensors():  # lux.luminance
    dht_1 = dht.DHTSensor.get_instance("indoor")
    dht_2 = dht.DHTSensor.get_instance("outdoor")
    lux_1 = bh1750.BH1750.get_instance("indoor")
    lux_2 = bh1750.BH1750.get_instance("outdoor")
    data = {"indoor": {"luminance": lux_1.luminance, "temperature": dht_1.temp, "humidity": dht_1.humid},
            "outdoor": {"luminance": lux_2.luminance, "temperature": dht_2.temp, "humidity": dht_2.humid}}
    return json.dumps(data)


@app.route('/api/stepper/get_status')
def status():
    msg = json.dumps({"status": step.Stepper.get_instance().allowed,
                      "steps": step.Stepper.get_instance().scheduled_steps,
                      "current_position": step.Stepper.get_instance().current_position,
                      "scheduled_position": step.Stepper.get_instance().scheduled_position,
                      "min_position": step.Stepper.get_instance().min_position,
                      "max_position": step.Stepper.get_instance().max_position})
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


@app.route('/api/stepper/set_max_position/<pos>')
def set_max_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().max_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().max_position})
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
    except (ValueError, TypeError):
        return json.dumps({"success": False, "value": None})
    return json.dumps({"success": True, "value": step.Stepper.get_instance().allowed})


@app.route('/test/api/sensors')
def test_sensors():
    dht_1_t = random.randint(20, 30)
    dht_1_h = random.randint(40, 60)
    dht_2_t = random.randint(15, 22)
    dht_2_h = random.randint(50, 65)
    lux_1 = random.randrange(3, 100)
    lux_2 = random.randrange(50, 100)
    data = {"indoor": {"luminance": lux_1, "temperature": dht_1_t, "humidity": dht_1_h},
            "outdoor": {"luminance": lux_2, "temperature": dht_2_t, "humidity": dht_2_h}}
    return json.dumps(data)
