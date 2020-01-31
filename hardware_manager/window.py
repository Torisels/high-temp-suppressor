import threading
from . import dht, bh1750, data_container
import time


class Window:
    POLL_TIME = 2
    _INSTANCE = None

    @classmethod
    def get_instance(cls):  # singleton, use this to create stepper motor instance for whole project
        if cls._INSTANCE is None:
            cls._INSTANCE = Window()
        return cls._INSTANCE

    def __init__(self):
        self.last_value = None
        t1 = threading.Thread(target=self.loop)
        t1.start()

    def loop(self):
        while True:
            if not data_container.DataContainer.get_instance().sensor_lock:
                indoor_t = dht.DHTSensor.get_instance("indoor")
                outdoor_t = dht.DHTSensor.get_instance("outdoor")
                outdoor_l = bh1750.BH1750.get_instance("outdoor")
                time.sleep(self.POLL_TIME)
                if indoor_t.temp and outdoor_t.temp and indoor_t.humid and outdoor_t.humid and outdoor_l.luminance:

                    d = self.decision(indoor_t.temp, outdoor_t.temp, indoor_t.humid, outdoor_t.humid, 0,
                                      outdoor_l.luminance)
                    if d != self.last_value:
                        self.last_value = d
                        data_container.DataContainer.get_instance().info.put(d)

            else:
                time.sleep(self.POLL_TIME)

    def decision(self, tin, tout, humin, humout, lightin, lightout, optimal1=21, optimal2=28):
        # Optimal temperature is usually claimed to be between 21°C - 28°C, but there is room for customization
        # Source: https://www.weather.gov/media/epz/wxcalc/heatIndex.pdf
        tin = 9 / 5 * tin + 32  # Fahrenheit conversion
        tout = 9 / 5 * tout + 32
        heatin = -42.379 + 2.04901523 * tin + 10.14333127 * humin - .22475541 * tin * humin - .00683783 * tin * tin \
                 - .05481717 * humin * humin + .00122874 * tin * tin * humin + .00085282 * tin * humin * humin \
                 - .00000199 * tin * tin * humin * humin  # Equation for apparent temperature

        heatout = -42.379 + 2.04901523 * tout + 10.14333127 * humout - .22475541 * tout * humout - .00683783 * tout * tout \
                  - .05481717 * humout * humout + .00122874 * tout * tout * humout + .00085282 * tout * humout * humout \
                  - .00000199 * tout * tout * humout * humout

        heatin = (heatin - 32) * (5 / 9)  # Celsius conversion
        heatout = (heatout - 32) * (5 / 9)
        s = 'Apparent temperature in a room equals to: ' + str(round(heatin, 2)) + "&#176;C." + '<br/>'
        if optimal2 > heatin > optimal1:
            if heatin > heatout and lightout > 35000:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to decrease temperature in the room, tilt the window.'
            elif heatin > heatout:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to decrease temperature in the room, open the window.'
            else:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to increase temperature in the room, open the window.'
        else:
            if heatin > optimal2:
                if heatin > heatout and lightout > 35000:
                    s += 'It is advised to tilt the window to achieve temperature closer to optimum range.'
                elif heatin > heatout:
                    s += 'It is advised to open the window achieve temperature closer to optimum range.'
                else:
                    s += 'It is not advised to open the window. It will only get hotter.'
            else:
                if heatin < heatout:
                    s += 'It is advised to open the window achieve temperature closer to optimum range.'
                else:
                    s += 'It is not advised to open the window. It will only get hotter.'
        return s
