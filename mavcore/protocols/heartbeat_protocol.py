from mavcore.mav_protocol import MAVProtocol
from mavcore.mav_sender import Sender
from mavcore.mav_receiver import Receiver
from mavcore.messages.heartbeat_msg import Heartbeat


class HeartbeatProtocol(MAVProtocol):
    """
    Protocol for sending consistent heartbeats. Automatically sends at 1 HZ. Defaults to GCS heartbeat type.
    """

    def __init__(self):
        super().__init__()
        self.heartbeat_msg = Heartbeat()

    def run(self, sender: Sender, receiver: Receiver):
        sender.send_msg(self.heartbeat_msg)

    def __repr__(self) -> str:
        return str(self.heartbeat_msg)
