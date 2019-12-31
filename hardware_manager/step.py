import RPi.GPIO as GPIO
import time
import threading


class Stepper:
    LOW = 0
    HIGH = 1
    FULL_ROTATION_FULL_STEP = int(
        4075.7728395061727 / 2)  # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html
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
        [HIGH, LOW, LOW, LOW],
        [LOW, HIGH, LOW, LOW],
        [LOW, LOW, HIGH, LOW],
        [LOW, LOW, LOW, HIGH]
    ]

    _INSTANCE = None
    PIN1 = 7
    PIN2 = 11
    PIN3 = 13
    PIN4 = 15
    PIN_EMERGENCY_STOP = 21
    DELAY = 4

    @classmethod
    def get_instance(cls):  # singleton, use this to create stepper motor instance for whole project
        if cls._INSTANCE is None:
            cls._INSTANCE = Stepper(cls.FULL_STEP, cls.PIN1, cls.PIN2, cls.PIN3, cls.PIN4, cls.PIN_EMERGENCY_STOP,
                                    cls.DELAY)
        return cls._INSTANCE

    def __init__(self, mode, pin1, pin2, pin3, pin4, pin_emergency_stop, delay):
        GPIO.setmode(GPIO.BCM)
        self.mode = mode
        self.pins = [pin1, pin2, pin3, pin4]
        self.delay = delay
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        self._scheduled_steps = 0
        if pin_emergency_stop is not None:
            self.pin_e_stop = pin_emergency_stop
            # self.pin_e_stop.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_emergency_stop)

        self.allowed = True
        self.reset()

        t1 = threading.Thread(target=self.loop)
        t1.start()
        t2 = threading.Thread(target=self.emergency_stop_handler)
        t2.start()

    @property
    def steps(self):
        return self._scheduled_steps

    @steps.setter
    def steps(self, steps):
        self._scheduled_steps += steps

    def emergency_stop_handler(self):  # TODO
        emergency_stop_button_down = False
        if emergency_stop_button_down:
            if self.allowed is True:
                self.allowed = False
                self.reset()

    def loop(self):
        while True:
            if self._scheduled_steps == 0 or self.allowed is False:
                # await asyncio.sleep(0.5)
                time.sleep(0.5)
                self.reset()
            elif self.allowed:
                # await self.mv_four_steps()
                self.mv_four_steps()

    def mv_four_steps(self):
        direction = 1 if self._scheduled_steps > 0 else -1
        bits_list = self.mode[::direction]
        for _ in range(abs(self._scheduled_steps)):
            if self.allowed:
                for bits in bits_list:
                    for bit, pin in zip(bits, self.pins):
                        GPIO.output(pin, bit)
                    # await asyncio.sleep(self.delay/1000)
                    time.sleep(self.delay / 1000)
                if direction == 1:
                    self._scheduled_steps -= 1
                else:
                    self._scheduled_steps += 1
            else:
                self.reset()
        self.reset()

    def reset(self):
        for pin in self.pins:
            GPIO.output(pin, 0)
