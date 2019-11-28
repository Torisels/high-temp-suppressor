from machine import Pin
from machine import Timer




class Encoder:
    """ Adapted from https://github.com/mathertel/RotaryEncoder and https://hackaday.io/project/13201-encoderlib
        Works with D0 and D6 for sure. There are some problems with D6 and D7 pins.
    """
    KNOB_DIR = [0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0]
    LATCH_STATE = 3

    def __init__(self, clk_pin, dt_pin):
        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt_pin, Pin.IN)
        self._oldState = 0
        self.position_ext = 0
        self.position_ext_prev = 0
        self.position = 0

        self.diff = 0

        tim = Timer(-1)
        tim2 = Timer(-1)
        tim.init(period=1, mode=Timer.PERIODIC, callback=self.update)
        # tim2.init(period=500, mode=Timer.PERIODIC, callback=self.get_diff())

    def get_value(self):
        return self.position_ext  # Return rotary encoder value

    def get_diff(self):
        diff = self.position_ext - self.position_ext_prev
        self.position_ext_prev = self.position_ext
        return diff

    def update(self, p):
        # Read the rotary encoder pins
        clk = self.clk.value()
        dt = self.dt.value()

        new_state = clk | (dt << 1)

        if self._oldState != new_state:

            pos = (new_state | (self._oldState << 2))
            self.position += self.KNOB_DIR[pos]
            if new_state == self.LATCH_STATE:
                self.position_ext = self.position >> 2
                self.diff += self.position_ext - self.position_ext_prev
                self.position_ext_prev = self.position_ext
            self._oldState = new_state
