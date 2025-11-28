from typing import Any, Callable
import time
import threading
import queue


def thread_safe(func):
    def wrapper(*args, **kwargs) -> Any:
        self : MAVMessage = args[0]
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
        non_blocking: bool = False,
    ):
        """
        Designed to be an interface/template for a MAVMessage:

        name: the mavlink message name to look for
        timestamp: the time in seconds the message was recieved
        priority: unused for now
        repeat_period: the interval at which the message will be repeatedly sent
        callback_func: a function that will be executed when this message is recieved and processed,
            this message instance is passed in to the first and only argument.
        non_blocking: if true, the callback function will be executed in a new thread
        """
        self.name = name
        self.timestamp = timestamp
        self.priority = priority
        self.repeat_period = repeat_period
        self.callback_func = callback_func
        self._lock = threading.Lock()
        self._thread: None | threading.Thread = None
        self.submessages: list[MAVMessage] = []
        # For calculating receive rate
        self.hz : float = 0.0 
        self._pastdt : list[float] = []
        '''
        Callback processing. Similar to ROS each listener has its own thread for processing messages so that
        one slow listener does not block others from being processed. There will be a queue of up to 15 messages
        for each listener. If the queue is full, the oldest message will be dropped.
        '''
        self._msg_queue : "queue.Queue[Any]" = queue.Queue(maxsize=15)
        self.end = False


    @thread_safe
    def update_timestamp(self, timestamp: float):
        """
        Thread-safe wrapper for updating the timestamp and calculating the receive rate (hz).
        Do not override this method.
        """
        if self.timestamp == 0.0:
            self.timestamp = timestamp
            return
        dt = timestamp - self.timestamp
        self._pastdt.append(dt)
        if len(self._pastdt) > 10:
            self._pastdt.pop(0)
        self.hz = len(self._pastdt) / sum(self._pastdt)
        self.timestamp = timestamp

    def _start_callback_thread(self):
        """
        Starts the internal thread for processing the decode and callback function. <br>
        Do not override this method.
        """
        if self._thread is not None and self._thread.is_alive():
            return  # Thread is already running
        self.end = False
        self._thread = threading.Thread(target=self._process, daemon=True)
        self._thread.start()

    def _process(self):
        """
        Internal method for processing the decode and callback function. <br>
        Do not override this method. TODO: Make thread safe and fix conflict with waiting messages
        """
        while not self.end:
            try:
                msg = self._msg_queue.get(timeout=0.1)
                self._decode(msg)
            except queue.Empty:
                continue

    @thread_safe
    def _encode(self, system_id, component_id) -> Any:
        """
        Thread-safe wrapper for encode. Do not override this method.
        """
        return self.encode(system_id, component_id)

    def encode(self, system_id, component_id) -> Any:
        """
        Returns this MAVMessage as a pymavlink friendly message.
        """
        pass
    
    @thread_safe
    def _decode(self, msg):
        """
        Thread-safe wrapper for decode. Do not override this method.
        """
        self.decode(msg)
        self.callback_func(self)

    def decode(self, msg):
        """
        Transforms this MAVMessage based off of a pymavlink message that was received.
        """
        pass

    def __repr__(self) -> str:
        return f"({self.name}) timestamp: {self.timestamp} ms"
    
    def __str__(self) -> str:
        return self.__repr__()

    def wait_until_finished(self):
        """
        Blocks until the internal thread is finished executing.
        """
        if type(self._thread) is not threading.Thread:
            return

        while self._thread.is_alive():
            time.sleep(0.1)
        self._thread = None

    def is_finished(self) -> bool:
        """
        Returns whether the internal thread is finished executing.
        """
        return self._thread is None
