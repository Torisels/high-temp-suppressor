# Inspired by http://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/
# Adapted by @Torisels (Gustaw Daczkowski) from "https://gist.github.com/oskar456/95c66d564c58361ecf9f"

from .pin_config import config
from smbus2 import smbus2
import time
import threading


class BH1750:
    """Singleton model section"""
    _INSTANCES = {"indoor": None, "outdoor": None}
    _BUS = smbus2.SMBus(1)

    @classmethod
    def get_instance(cls, name):
        if cls._INSTANCES[name] is None:
            cls._INSTANCES[name] = BH1750(cls._BUS, config[cls.__name__][name])
        return cls._INSTANCES[name]

    """ Implement BH1750 communication. """
    # Define some constants from the data sheet
    POWER_DOWN = 0x00  # No active state
    POWER_ON = 0x01  # Power on
    RESET = 0x07  # Reset data register value
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23

    DEFAULT_SENSITIVITY = 200

    def __init__(self, bus, address=0x23):
        self.bus = bus
        self.addr = address
        self.power_off()
        self.set_sensitivity(self.DEFAULT_SENSITIVITY)
        self._value = -1
        t = threading.Thread(target=self.loop)
        t.start()

    @property
    def luminance(self):
        return self._value

    def loop(self):
        while True:
            self._value = round(self.measure_high_res2(), 2)

    def _set_mode(self, mode):
        self.mode = mode
        self.bus.write_byte(self.addr, self.mode)

    def power_off(self):
        self._set_mode(self.POWER_DOWN)

    def power_on(self):
        self._set_mode(self.POWER_ON)

    def reset(self):
        self.power_on()  # It has to be powered on before resetting
        self._set_mode(self.RESET)

    def set_sensitivity(self, sensitivity=69):
        """ Set the sensor sensitivity.
            Valid values are 31 (lowest) to 254 (highest), default is 69.
        """
        if sensitivity < 31:
            self.mtreg = 31
        elif sensitivity > 254:
            self.mtreg = 254
        else:
            self.mtreg = sensitivity
        self.power_on()
        self._set_mode(0x40 | (self.mtreg >> 5))
        self._set_mode(0x60 | (self.mtreg & 0x1f))
        self.power_off()

    def get_result(self):
        """ Return current measurement result in lx. """
        data = self.bus.read_word_data(self.addr, self.mode)
        count = data >> 8 | (data & 0xff) << 8
        mode2_coefficient = 2 if (self.mode & 0x03) == 0x01 else 1
        ratio = 1 / (1.2 * (self.mtreg / 69.0) * mode2_coefficient)
        return ratio * count

    def wait_for_result(self, additional=1):
        base_time = 0.018 if (self.mode & 0x03) == 0x03 else 0.128
        time.sleep(base_time * (self.mtreg / 69.0) + additional)

    def do_measurement(self, mode, additional_delay=0):
        """ 
        Perform complete measurement using command
        specified by parameter mode with additional
        delay specified in parameter additional_delay.
        Return output value in Lx.
        """
        self.reset()
        self._set_mode(mode)
        self.wait_for_result(additional_delay)
        return self.get_result()

    def measure_low_res(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_LOW_RES_MODE, additional_delay)

    def measure_high_res(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_1, additional_delay)

    def measure_high_res2(self, additional_delay=0):
        return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_2, additional_delay)


