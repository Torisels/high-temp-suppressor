import Adafruit_DHT as dht
import time
import RPi.GPIO as GPIO
import threading
from .pin_config import config
from . import data_container

class DHTSensor:
    _INSTANCES = {"indoor": None, "outdoor": None}
    POLL_TIME = 1.5

    @classmethod
    def get_instance(cls, name):
        if cls._INSTANCES[name] is None:
            cls._INSTANCES[name] = DHTSensor(config[cls.__name__][name])
        return cls._INSTANCES[name]

    def __init__(self, data_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(data_pin, GPIO.IN)
        self.data_pin = data_pin
        self._temp = None
        self._humid = None
        t1 = threading.Thread(target=self.loop)
        t1.start()

    @property
    def temp(self):
        return self._temp

    @property
    def humid(self):
        return self._humid

    def loop(self):
        while True:
            if not data_container.DataContainer.get_instance().sensor_lock:
                humid, temp = dht.read(dht.DHT11, self.data_pin)
                self._humid = humid if humid else self._humid
                self._temp = temp if temp else self._temp
            time.sleep(self.POLL_TIME)
