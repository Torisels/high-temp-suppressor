import network
import tinyweb
import gc
import step

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
        step.steps = st
        msg = "{success: %s, value: %d}" % ("True", st)
    except ValueError:
        msg = "{success: %s, value: %d}" % ("False", None)
    resp.add_header("Content-Type", "application/json")
    gc.collect()
    await resp._send_headers()
    await resp.send(msg)


@app.route('/api/get_status')
async def status(req: tinyweb.server.request, resp: tinyweb.server.response):
    resp.add_header("Content-Type", "application/json")
    await resp._send_headers()
    gc.collect()
    await resp.send("{" + 'status: {}, steps: {}'.format(step.Stepper.get_instance().allowed, step.steps) + "}")


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
    # ap = network.WLAN(network.AP_IF)
    # ap.active(True)
    # ap.config(essid="Siec", password="123123123")
    # print(ap.ifconfig()[0])
    # Set all pins to OUT mode
    # for p, d in pins.items():
    #     machine.Pin(p, machine.Pin.OUT)

    app.add_resource(Status, '/api/status')
    # app.add_resource(GPIOList, '/api/gpio')
    # app.add_resource(GPIO, '/api/gpio/<pin>')
    # app.add_resource(StepperController, '/api/stepper')
    s = step.Stepper.get_instance()
    app.run(host='0.0.0.0', port=8081)


if __name__ == '__main__':
    run()
