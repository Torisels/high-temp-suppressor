import RPi.GPIO as GPIO
import time
import threading
import json
import os

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
    CONFIG_PATH = 'stepper_config.json'
    DEFAULT_CONFIG = {
        'min_position': 0,
        'max_position': 1000,
        'current_position': 0
    }
    CONFIG_SAVE_DELAY = 1  # seconds

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
        if pin_emergency_stop is not None:
            self.pin_e_stop = pin_emergency_stop
            # self.pin_e_stop.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_emergency_stop)
        self.allowed = True
        self._scheduled_steps = 0
        self._step_mode = False         # True - scheduled steps does not affect current position
        self._max_position = 0
        self._min_position = 0
        self._current_position = 0
        try:
            self._read_config()
        except Exception as err:
            print("error reading a stepper config, setting default values \n" + str(err))
            self._update_config_from_dict(self.DEFAULT_CONFIG)

        self._scheduled_position = self._current_position

        self.reset()
        t1 = threading.Thread(target=self.loop)
        t1.start()
        t2 = threading.Thread(target=self.emergency_stop_handler)
        t2.start()
        t3 = threading.Thread(target=self.config_save_loop)
        t3.start()
        
    def config_save_loop(self):
        while True:
            time.sleep(self.CONFIG_SAVE_DELAY)
            try:
                self._save_config()
            except ValueError as err:
                print(err)
    
    def _get_config_dict(self):
        return {
            'max_position': self._max_position,
            'min_position': self._min_position,
            'current_position': self._current_position
        }
    
    def _update_config_from_dict(self, conf):
        tmp_max = conf['max_position']
        tmp_min = conf['min_position']
        tmp_cur = conf['current_position']
        if tmp_min > tmp_max:
            raise ValueError("max position cannot be smaller than min position")
        self._max_position = tmp_max
        self._min_position = tmp_min
        self.current_position = tmp_cur

    def _read_config(self, path = CONFIG_PATH):
        with open(path) as json_file:
            data = json.load(json_file)
        self._update_config_from_dict(data)
    
    def _save_config(self, path = CONFIG_PATH):
        if os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(self._get_config_dict(), f)
        else:
            raise ValueError("such path does not exist")
    
    @property
    def max_position(self):
        return self._max_position

    @max_position.setter
    def max_position(self, pos):
        if pos < self._min_position:
            raise ValueError("max position cannot be smaller than min position")
        if self._current_position > pos:
            self.current_position = pos
        self._max_position = pos

    @property
    def min_position(self):
        return self._min_position
    
    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, new_position):
        if new_position < self.min_position or new_position > self.max_position:
            raise ValueError("new position is out of range")
        self.reset()
        self._reset_step_mode()
        self._current_position = new_position
        self._scheduled_position = new_position
   
    @property
    def scheduled_position(self):
        return self._scheduled_position

    @scheduled_position.setter
    def scheduled_position(self, new_position):
        if new_position < self.min_position or new_position > self.max_position:
            raise ValueError("new position is out of range")
        self.reset()
        self._reset_step_mode()
        self._scheduled_position = new_position
        
    def _reset_step_mode(self):
        self._step_mode = False
        self._scheduled_steps = 0
        time.sleep(self.delay*5 / 1000)

    
    @property
    def scheduled_steps(self):
        if self._scheduled_steps != 0:
            self._step_mode = True
            self._scheduled_position = self._current_position
            return self._scheduled_steps
        return self._scheduled_position - self._current_position
    
    @scheduled_steps.setter
    def scheduled_steps(self, new_value):
        self._step_mode = True
        self._scheduled_steps = new_value

    def emergency_stop_handler(self):  # TODO
        emergency_stop_button_down = False
        if emergency_stop_button_down:
            if self.allowed is True:
                self.allowed = False
                self.reset()

    def loop(self):
        while True:
            if self.scheduled_steps == 0 or self.allowed is False:
                time.sleep(0.5)
                self.reset()
            elif self.allowed:
                self.mv_four_steps()

    def mv_four_steps(self):
        direction = 1 if self.scheduled_steps > 0 else -1
        bits_list = self.mode[::direction]
        #while self.scheduled_steps != 0:
        if self.allowed:
            for bits in bits_list:
                for bit, pin in zip(bits, self.pins):
                    GPIO.output(pin, bit)
                # await asyncio.sleep(self.delay/1000)
                time.sleep(self.delay / 1000)
            if self._step_mode:
                self._scheduled_steps -= direction
            else:
                self._current_position += direction
        #else:
        #    self.reset()
        self.reset()

    def reset(self):
        for pin in self.pins:
            GPIO.output(pin, 0)
