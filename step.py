from machine import Pin
import time
import uasyncio as asyncio
import utime


steps = 0


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
    PIN1 = 15
    PIN2 = 13
    PIN3 = 14
    PIN4 = 2
    DELAY = 3
    PIN_EMERGENCY_STOP = 12

    @classmethod
    def get_instance(cls):  # singleton, use this to create stepper motor instance for whole project
        if cls._INSTANCE is None:
            cls._INSTANCE = Stepper(cls.FULL_STEP, cls.PIN1, cls.PIN2, cls.PIN3, cls.PIN4, cls.PIN_EMERGENCY_STOP,
                                    cls.DELAY)
        return cls._INSTANCE

    def __init__(self, mode, pin1, pin2, pin3, pin4, pin_emergency_stop, delay):
        self.mode = mode
        self.pins = [Pin(pin1, Pin.OUT), Pin(pin2, Pin.OUT), Pin(pin3, Pin.OUT), Pin(pin4, Pin.OUT)]
        self.delay = delay

        self._scheduled_steps = 0
        if pin_emergency_stop:
            self.pin_e_stop = Pin(pin_emergency_stop, Pin.IN, Pin.PULL_UP)
            self.pin_e_stop.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_emergency_stop)

        self.allowed = True
        self.reset()

        loop = asyncio.get_event_loop()
        loop.create_task(self.loop())

    @property
    def steps(self):
        return self._scheduled_steps

    @steps.setter
    def steps(self, steps):
        self._scheduled_steps += steps

    def handle_emergency_stop(self, i):
        if self.allowed is True:
            self.allowed = False
            print("Emergency_stop_occured")
            self.reset()

    # async def loop(self):
    #     while True:
    #         global steps
    #         if steps == 0 or self.allowed is False:
    #             await asyncio.sleep_ms(500)
    #             self.reset()
    #         elif self.allowed:
    #             if steps > 0:
    #                 await self.step(steps, 1)
    #             else:
    #                 await self.step(steps, -1)
    async def loop(self):
        while True:
            if self._scheduled_steps == 0 or self.allowed is False:
                await asyncio.sleep_ms(500)
                self.reset()
            elif self.allowed:
                await self.mv_four_steps()

    def move_one_step(self, direction):
        if self.allowed:
            # print(self.step_pointer)
            bits = self.mode[self.step_pointer]
            for bit, pin in zip(bits, self.pins):
                pin.value(bit)
        else:
            print("moving not allowed!")
            self.reset()
        if direction == 1:
            if self.step_pointer == 3:
                self.step_pointer = 0
            else:
                self.step_pointer += 1
        elif direction == -1:
            if self.step_pointer == 0:
                self.step_pointer = 3
            else:
                self.step_pointer -= 1
        # await asyncio.sleep_ms(self.delay)

    async def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        divisor = 4 if self.mode == self.FULL_STEP else 8
        count, remainder = divmod(count, divisor)

        iterations = [(count, len(self.mode) + 1), (1, remainder)]
        bits_list = self.mode[::direction]

        for count, remainder in iterations:
            for _ in range(count):
                for bits in bits_list[:remainder]:
                    if self.allowed:
                        global steps
                        if steps > 0:
                            steps -= 1
                        elif steps < 0:
                            steps += 1
                        for bit, pin in zip(bits, self.pins):
                            pin.value(bit)
                        await asyncio.sleep_ms(self.delay + 1)
                    else:
                        self.reset()
                        return False
        self.reset()

    async def mv_four_steps(self):
        direction = 1 if self._scheduled_steps > 0 else -1
        bits_list = self.mode[::direction]
        for _ in range(abs(self._scheduled_steps)):
            if self.allowed:
                for bits in bits_list:
                    for bit, pin in zip(bits, self.pins):
                        pin.value(bit)
                    await asyncio.sleep_ms(self.delay)
                if direction==1:
                    self._scheduled_steps -= 1
                else:
                    self._scheduled_steps += 1
            else:
                self.reset()
        self.reset()

    # async def mv_four_steps_async(self, times, direction=1):
    #     bits_list = self.mode[::direction]
    #     for _ in range(abs(times)):
    #         for bits in bits_list:
    #             for bit, pin in zip(bits, self.pins):
    #                 pin.value(bit)
    #             await asyncio.sleep_ms(self.delay)
    #     self.reset()

    def reset(self):
        for pin in self.pins:
            pin.off()


def rn(times=Stepper.FULL_ROTATION_FULL_STEP, delay=2, dir=1):
    s1 = Stepper(Stepper.FULL_STEP, 15, 13, 14, 2, None, delay)
    start = time.time()
    s1.mv_four_steps(times, dir)
    end = time.time()
    print(end - start)
