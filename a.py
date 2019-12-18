import network
import tinyweb
import gc
import step
import json
from machine import Pin
from machine import I2C
from light_sensor import LightSensor
app = tinyweb.server.webserver()


# Index page
@app.route('/')
@app.route('/index.html')
async def index(req, resp):
    await resp.send_file('static/index.html')


# JS files.
# Since ESP8266 is low memory platform - it totally make sense to
# pre-gzip all large files (>1k) and then send gzipped version
@app.route('/js/<fn>')
async def files_js(req, resp, fn):
    await resp.send_file('static/js/{}.gz'.format(fn),
                         content_type='application/javascript',
                         content_encoding='gzip')


# The same for css files - e.g.
# Raw version of bootstrap.min.css is about 146k, compare to gzipped version - 20k
@app.route('/css/<fn>')
async def files_css(req, resp, fn):
    await resp.send_file('static/css/{}.gz'.format(fn),
                         content_type='text/css',
                         content_encoding='gzip')


# Images
@app.route('/images/<fn>')
async def files_images(req, resp, fn):
    await resp.send_file('static/images/{}'.format(fn),
                         content_type='image/jpeg')


@app.route('/api/set_steps/<st>')
async def move(req, resp, st):
    try:
        st = int(st)
        step.Stepper.get_instance().steps = st
        msg = "{success: %s, value: %d}" % ("True", step.Stepper.get_instance().steps )
    except ValueError:
        msg = "{success: %s, value: %d}" % ("False", None)

    resp.add_header("Content-Type", "application/json")
    # resp.add_header("Access-Control-Allow-Origin", "null")
    gc.collect()
    await resp._send_headers()
    await resp.send(msg)


@app.route('/api/get_status')
async def status(req: tinyweb.server.request, resp: tinyweb.server.response):
    resp.add_header("Content-Type", "application/json")
    resp.add_header("Access-Control-Allow-Origin", "null")
    await resp._send_headers()
    res = json.dumps({"status": str(step.Stepper.get_instance().allowed), "steps":step.Stepper.get_instance().steps})
    await resp.send(res)
    gc.collect()


@app.route('/api/set_status/<val>')
async def move(req: tinyweb.server.request, resp: tinyweb.server.response, val):
    try:
        v = int(val)
        if v:
            step.Stepper.get_instance().allowed = True
        else:
            step.Stepper.get_instance().allowed = False
    except ValueError:
        pass

    resp.add_header("Content-Type", "application/json")
    resp.add_header("Access-Control-Allow-Origin", "null")
    await resp._send_headers()
    await resp.send("{" + 'status: {}'.format( step.Stepper.get_instance().allowed) + "}")
    gc.collect()


# RESTAPI: System status
class Status():

    def get(self, data):
        mem = {'mem_alloc': gc.mem_alloc(),
               'mem_free': gc.mem_free(),
               'mem_total': gc.mem_alloc() + gc.mem_free()}
        sta_if = network.WLAN(network.STA_IF)
        ifconfig = sta_if.ifconfig()
        net = {'ip': ifconfig[0],
               'netmask': ifconfig[1],
               'gateway': ifconfig[2],
               'dns': ifconfig[3]
               }
        return {'memory': mem, 'network': net}


def run():

    app.add_resource(Status, '/api/status')
    s = step.Stepper.get_instance()
    scl = Pin(5)
    sda = Pin(4)
    i2c = I2C(scl, sda)
    l_s = LightSensor(i2c)
    app.run(host='0.0.0.0', port=8081)


if __name__ == '__main__':
    run()
