from machine import Pin
import time


class Encoder1:
    KNOBDIR = [0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0]
    LATCHSTATE = 3

    def __init__(self, pin1, pin2):
        self._pin1 = Pin(pin1, Pin.IN, Pin.PULL_UP)
        self._pin2 = Pin(pin2, Pin.IN, Pin.PULL_UP)

        self._oldState = 0
        self._position = 5
        self._positionExt = 0

    def get_pos(self):
        return self._positionExt

    def tick(self):
        sig1 = self._pin1.value()
        sig2 = self._pin2.value()
        # print(("Sig1 {}").format(sig1))
        # print("Sig2 {}".format(sig2))
        thisState = sig1 | (sig2 << 1)

        if self._oldState != thisState:
            pos = (thisState | (self._oldState << 2))
            # print(pos)
            self._position += self.KNOBDIR[pos]
            if thisState == 3:
                self._positionExt = self._position // 4
                # print(self._positionExt)
            self._oldState = thisState


