import queue
import threading
import time

from mavcore.mav_message import MAVMessage

MAX_QUEUE_SIZE = 500
HISTORY_SIZE = 10


class Receiver:
    def __init__(self, listeners: list[MAVMessage]):
        self.history_dict: dict[str, list] = {}
        self.queue = queue.Queue()
        self.listeners = listeners
        self.waiting: list[MAVMessage] = []
        self.receiving = False

    def start_receiving(self):
        self.receiving = True
        self._thread = threading.Thread(target=self.process, daemon=True)
        self._thread.start()

    def stop_receiving(self):
        self.receiving = False

    def process(self):
        while self.receiving:
            timestamp_ms, msg = self.queue.get()
            msg_name = msg.get_type()

            # Check if waiting for this message
            found = []
            for wait_msg in self.waiting:
                if wait_msg.name == msg_name:
                    wait_msg.timestamp = timestamp_ms
                    wait_msg.decode(msg)
                    wait_msg.process()
                    found.append(wait_msg)
            for m in found:
                self.waiting.remove(m)

            # Update listeners
            for listener in self.listeners:
                if listener.name == msg_name and listener.timestamp != timestamp_ms:
                    listener.timestamp = timestamp_ms
                    listener.decode(msg)
                    listener.process()

            # Manage message history
            if msg_name in self.history_dict:
                self.history_dict[msg_name].insert(0, (timestamp_ms, msg))

                # Manage history length
                if len(self.history_dict[msg_name]) > HISTORY_SIZE:
                    self.history_dict[msg_name].pop()
            else:
                # Brand new message type
                self.history_dict[msg_name] = [(timestamp_ms, msg)]

    def wait_for_msg(
        self, msg: MAVMessage, timeout_seconds: float = -1.0, blocking=True
    ) -> MAVMessage:
        """
        Will wait for msg to occur. Once it does, will return the updated object.
        If blocking will return a FutureMsg.
        """
        if not blocking:
            msg._thread = threading.Thread(
                target=lambda: self.wait_for_msg(msg), daemon=True
            )
            msg._thread.start()
            return msg

        timeout_timer = time.time()
        msg.timestamp = 0.0
        self.waiting.append(msg)
        while msg.timestamp == 0.0 and (
            timeout_seconds < 0 or time.time() - timeout_timer < timeout_seconds
        ):
            time.sleep(0.001)

        try:
            self.waiting.remove(msg)
        except Exception:
            pass

        return msg
