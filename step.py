from machine import Pin
# (c) IDWizard 2017
# MIT License.
import utime
import time


LOW = 0
HIGH = 1
FULL_ROTATION_FULL_STEP = int(4075.7728395061727 / 2)  # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html
FULL_ROTATION_HALF_STEP = int(4075.7728395061727)  # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html

HALF_STEP = [
    [LOW, LOW, LOW, HIGH],
    [LOW, LOW, HIGH, HIGH],
    [LOW, LOW, HIGH, LOW],
    [LOW, HIGH, HIGH, LOW],
    [LOW, HIGH, LOW, LOW],
    [HIGH, HIGH, LOW, LOW],
    [HIGH, LOW, LOW, LOW],
    [HIGH, LOW, LOW, HIGH],
]

FULL_STEP = [
    [HIGH, LOW, HIGH, LOW],
    [LOW, HIGH, HIGH, LOW],
    [LOW, HIGH, LOW, HIGH],
    [HIGH, LOW, LOW, HIGH]
]


class Stepper:
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay=2):
        self.mode = mode
        self.pins = [Pin(pin1, Pin.OUT), Pin(pin2, Pin.OUT), Pin(pin3, Pin.OUT), Pin(pin4, Pin.OUT)]
        self.delay = delay  # Recommend 10+ for FULL_STEP, 1 is OK for HALF_STEP

        # Initialize all to 0
        self.reset()

    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        divisor = 4 if self.mode == FULL_STEP else 8
        count, remainder = divmod(count, divisor)

        iterations = [(count, len(self.mode) + 1), (1, remainder)]
        bits_list = self.mode[::direction]

        for count, remainder in iterations:
            for _ in range(count):
                for bits in bits_list[:remainder]:
                    for bit, pin in zip(bits, self.pins):
                        pin.value(bit)
                    utime.sleep_ms(self.delay)
        self.reset()

    def reset(self):
        for pin in self.pins:
            pin.off()


def rn(times=FULL_ROTATION_FULL_STEP, delay=2, dir=1):
    s1 = Stepper(FULL_STEP, 13, 12, 14, 2, delay=delay)
    start = time.time()
    s1.step(times, dir)
    end = time.time()
    print(end - start)

