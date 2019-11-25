from machine import Pin


class Encoder:
    KNOBDIR = [0, -1, 1, 0,
               1, 0, 0, -1,
               -1, 0, 0, 1,
               0, 1, -1, 0]
    LATCHSTATE = 3

    def __init__(self, pin1, pin2):
        self._pin1 = Pin(pin1, Pin.IN, Pin.PULL_UP)
        self._pin2 = Pin(pin2, Pin.IN, Pin.PULL_UP)

        self._oldState = 3
        self._position = 0
        self._positionExt = 0
        self._positionExtPrev = 0

    def get_pos(self):
        return self._positionExt

    def tick(self):
        sig1 = self._pin1.value()
        sig2 = self._pin2.value()

        new_state = sig1 | (sig2 << 1)

        if self._oldState != new_state:
            self._position += self.KNOBDIR[new_state | (self._oldState << 2)]
            if new_state == self.LATCHSTATE:
                self._positionExt = self._position >> 2
            self._oldState = new_state


