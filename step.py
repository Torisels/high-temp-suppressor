from machine import Pin
# (c) IDWizard 2017
# MIT License.
import utime
import time

LOW = 0
HIGH = 1
FULL_ROTATION = int(4075.7728395061727 / 8)  # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html

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


class Command():
    """Tell a stepper to move X many steps in direction"""

    def __init__(self, stepper, steps, direction=1):
        self.stepper = stepper
        self.steps = steps
        self.direction = direction


class Driver():
    """Drive a set of motors, each with their own commands"""
    pass
    # @staticmethod
    # def run(commands):
    #     """Takes a list of commands and interleaves their step calls"""
    #
    #     # Work out total steps to take
    #     max_steps = sum([c.steps for c in commands])
    #
    #     count = 0
    #     while count != max_steps:
    #         for command in commands:
    #             # we want to interleave the commands
    #             if command.steps > 0:
    #                 command.stepper.step(1, command.direction)
    #                 command.steps -= 1
    #                 count += 1


class Stepper():
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay=2):
        self.mode = mode
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin2 = Pin(pin2, Pin.OUT)
        self.pin3 = Pin(pin3, Pin.OUT)
        self.pin4 = Pin(pin4, Pin.OUT)
        self.delay = delay  # Recommend 10+ for FULL_STEP, 1 is OK for HALF_STEP

        # Initialize all to 0
        self.reset()

    # def step(self, count, direction=1):
    #     """Rotate count steps. direction = -1 means backwards"""
    #     #
    #     # if self.mode == FULL_STEP:
    #     # c = 0
    #     # while c < count:
    #     #     index = c % 4
    #     #     self.pin1.value(self.mode[index][0])
    #     #     self.pin2.value(self.mode[index][1])
    #     #     self.pin3.value(self.mode[index][2])
    #     #     self.pin4.value(self.mode[index][3])
    #     #     c += 1
    #     #     utime.sleep_ms(self.delay)
    #
    #     if count % 2 == 0:
    #         for _ in range(count/2):
    #             for bit in self.mode[::direction]:
    #                 self.pin1.value(bit[0])
    #                 self.pin2.value(bit[1])
    #                 self.pin3.value(bit[2])
    #                 self.pin4.value(bit[3])
    #                 utime.sleep_ms(self.delay)
    #     else:
    #         times = count//2
    #         for _ in range(times):
    #             for bit in self.mode[::direction]:
    #                 self.pin1.value(bit[0])
    #                 self.pin2.value(bit[1])
    #                 self.pin3.value(bit[2])
    #                 self.pin4.value(bit[3])
    #                 utime.sleep_ms(self.delay)
    #         for bit in self.mode[:2:direction]:
    #             self.pin1.value(bit[0])
    #             self.pin2.value(bit[1])
    #             self.pin3.value(bit[2])
    #             self.pin4.value(bit[3])
    #             utime.sleep_ms(self.delay)
    #
    #     self.reset()

    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        count, remainder = divmod(count, 2)
        for _ in range(count):
            for bit in self.mode[::direction]:
                self.pin1.value(bit[0])
                self.pin2.value(bit[1])
                self.pin3.value(bit[2])
                self.pin4.value(bit[3])
                utime.sleep_ms(self.delay)
        if remainder == 1:
            for bit in self.mode[:2:direction]:
                self.pin1.value(bit[0])
                self.pin2.value(bit[1])
                self.pin3.value(bit[2])
                self.pin4.value(bit[3])
                utime.sleep_ms(self.delay)
        self.reset()

    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        self.pin1.off()
        self.pin2.off()
        self.pin3.off()
        self.pin4.off()


def rn(times = 10, delay = 2):
    s1 = Stepper(FULL_STEP, 13, 12, 14, 2, delay=delay)
    s1.step(times, 1)
    # runner = Driver()
    # runner.run([Command(s1, FULL_ROTATION*2, 1)])
