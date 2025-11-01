from typing import Any, Callable
import time
import threading


def thread_safe(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        self._lock.acquire()
        output = func(*args, **kwargs)
        self._lock.release()
        return output

    return wrapper


class MAVMessage:
    def __init__(
        self,
        name: str,
        timestamp: float = 0.0,
        priority=0,
        repeat_period: float = 0.0,
        callback_func: Callable[[Any], None] = lambda msg: None,
    ):
        """
        Designed to be an interface/template for a MAVMessage:

        name: the mavlink message name to look for
        timestamp: the time in miliseconds the message was recieved
        priority: unused for now
        repeat_period: the interval at which the message will be repeatedly sent
        callback_func: a function that will be executed when this message is recieved and processed,
            this message instance is passed in to the first and only argument.
        """
        self.name = name
        self.timestamp = timestamp
        self.priority = priority
        self.repeat_period = repeat_period
        self.callback_func = callback_func
        self._thread: None | threading.Thread = None
        self._lock = threading.Lock()

    def process(self):
        """
        automatically executes in main loop when receiving this message.
        """
        self.callback_func(self)

    def encode(self, system_id, component_id) -> Any:
        """
        Returns this MAVMessage as a pymavlink friendly message.
        """
        pass

    def decode(self, msg):
        """
        Transforms this MAVMessage based off of a pymavlink message that was received.
        """
        pass

    def __repr__(self) -> str:
        return f"({self.name}) timestamp: {self.timestamp} ms"

    def wait_until_finished(self):
        if type(self._thread) is not threading.Thread:
            return

        while self._thread.is_alive():
            time.sleep(0.1)
        self._thread = None

    def is_finished(self) -> bool:
        return self._thread is None
