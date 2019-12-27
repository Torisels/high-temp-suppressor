import Adafruit_DHT as dht 
import time
import RPi.GPIO as GPIO
import threading

class DHSensor:
    _INSTANCE = None
    DATA_PIN = 20
    
    @classmethod
    def get_instance(cls): 
        if cls._INSTANCE is None:
            cls._INSTANCE = DHSensor(cls.DATA_PIN)
        return cls._INSTANCE
        
    def __init__(self, data_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(data_pin, GPIO.IN)
        self.data_pin = data_pin
        self._temp = 0
        self._humid = 0
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
            self._temp, self._humid = dht.read(dht.DHT11, self.data_pin)
            time.sleep(1)
