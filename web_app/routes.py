from flask import render_template, send_from_directory, Response, request
from web_app import app
from hardware_manager import step
from hardware_manager import dht
from hardware_manager import bh1750
from hardware_manager import window
import json
import random
from queue import Queue

from hardware_manager import data_container


def event_stream():
    while True:
        message = data_container.DataContainer.get_instance().q.get(True)
        message = json.dumps(message)
        print("Sending {}".format(message))
        yield "data: {}\n\n".format(message)


@app.route('/api/stream')
def stream():
    resp = Response(event_stream(), mimetype="text/event-stream")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def msg_stream():
    while True:
        message = data_container.DataContainer.get_instance().info.get(True)
        message = {"msg": message}
        message = json.dumps(message)
        print("Sending {}".format(message))
        yield "data: {}\n\n".format(message)


@app.route('/api/msg')
def ms_stream():
    resp = Response(msg_stream(), mimetype="text/event-stream")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/message')
def message():
    message = window.Window.get_instance().last_value
    message = json.dumps({"msg": message})
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(message)
    return resp


# @app.route('/api/post', methods=['GET'])
# def api_parse_sentence():
#     queue.put(request.args.get('sentence'))
#     return "OK"

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
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(json.dumps(data))
    return resp


@app.route('/api/stepper/get_status')
def status():
    msg = json.dumps({"status": step.Stepper.get_instance()._allowed,
                      "steps": step.Stepper.get_instance().scheduled_steps,
                      "current_position": step.Stepper.get_instance().current_position,
                      "scheduled_position": step.Stepper.get_instance().scheduled_position,
                      "min_position": step.Stepper.get_instance().min_position,
                      "max_position": step.Stepper.get_instance().max_position})

    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(msg)
    return resp


@app.route('/api/stepper/set_position/<pos>')
def new_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().scheduled_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().scheduled_position})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})

    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(msg)
    return resp


@app.route('/api/stepper/set_max_position/<pos>')
def set_max_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().max_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().max_position})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(msg)
    return resp


@app.route('/api/stepper/set_steps/<st>')
def set_steps(st):
    try:
        st = int(st)
        step.Stepper.get_instance().scheduled_steps = st
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().scheduled_steps})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})

    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(msg)
    return resp


@app.route('/api/stepper/set_current_position/<pos>')
def set_current_position(pos):
    try:
        pos = int(pos)
        step.Stepper.get_instance().current_position = pos
        msg = json.dumps({"success": True, "value": step.Stepper.get_instance().current_position})
    except ValueError:
        msg = json.dumps({"success": False, "value": None})

    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(msg)
    return resp


@app.route('/api/stepper/set_status/<int:val>')
def set_status(val):
    try:
        step.Stepper.get_instance().allowed = bool(int(val))
        data = json.dumps({"success": True, "value": step.Stepper.get_instance().allowed})
    except (ValueError, TypeError):
        data = json.dumps({"success": False, "value": None})

    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.set_data(data)
    return resp

# @app.route('/test/api/sensors')
# def test_sensors():
#     dht_1_t = random.randint(20, 30)
#     dht_1_h = random.randint(40, 60)
#     dht_2_t = random.randint(15, 22)
#     dht_2_h = random.randint(50, 65)
#     lux_1 = random.randrange(3, 100)
#     lux_2 = random.randrange(50, 100)
#     data = {"indoor": {"luminance": lux_1, "temperature": dht_1_t, "humidity": dht_1_h},
#             "outdoor": {"luminance": lux_2, "temperature": dht_2_t, "humidity": dht_2_h}}
#     return json.dumps(data)
