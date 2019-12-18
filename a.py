import tinyweb
import gc
import step
import json
from machine import Pin
from machine import I2C
from light_sensor import LightSensor
import uasyncio as asyncio
import dht


class DHSensor:
    def __init__(self, data_pin):
        self.d = dht.DHT11(Pin(data_pin))
        self.temp = 0
        self.humid = 0
        loop = asyncio.get_event_loop()
        loop.create_task(self.loop())

    async def loop(self):
        while True:
            await asyncio.sleep_ms(1000)
            self.d.measure()
            self.temp = self.d.temperature()
            self.humid = self.d.humidity()


app = tinyweb.server.webserver(request_timeout=2, max_concurrency=2)
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
lux_1 = LightSensor(i2c)
dht11_1 = DHSensor(16)


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
        msg = "{success: %s, value: %d}" % ("True", step.Stepper.get_instance().steps)
    except ValueError:
        msg = "{success: %s, value: %d}" % ("False", None)

    resp.add_header("Content-Type", "application/json")
    # resp.add_header("Access-Control-Allow-Origin", "null")

    await resp._send_headers()
    await resp.send(msg)
    gc.collect()


@app.route('/api/get_status')
async def status(req: tinyweb.server.request, resp: tinyweb.server.response):
    resp.add_header("Content-Type", "application/json")
    # resp.add_header("Access-Control-Allow-Origin", "null")
    await resp._send_headers()
    res = json.dumps({"status": str(step.Stepper.get_instance().allowed), "steps": step.Stepper.get_instance().steps})
    await resp.send(res)
    gc.collect()


@app.route('/api/sensors')
async def sensors(req: tinyweb.server.request, resp: tinyweb.server.response):
    resp.add_header("Content-Type", "application/json")
    # resp.add_header("Access-Control-Allow-Origin", "null")
    await resp._send_headers()
    res = json.dumps({"lux1": lux_1.luminance, "temp1": dht11_1.temp, "hum1": dht11_1.humid})
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
    await resp.send("{" + 'status: {}'.format(step.Stepper.get_instance().allowed) + "}")
    gc.collect()


def run():
    step.Stepper.get_instance()
    app.run(host='0.0.0.0', port=8081)


if __name__ == '__main__':
    run()
