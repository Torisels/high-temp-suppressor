import queue


class DataContainer:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = DataContainer()
            return cls._INSTANCE
        return cls._INSTANCE

    def __init__(self):
        self.q = queue.Queue()
        self.sensor_lock = True
        self.info = queue.Queue()
