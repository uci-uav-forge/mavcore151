import time
from mavcore.messages.command_ack_msg import CommandAck
from pymavlink.dialects.v20 import common as mav

from mavcore.mav_protocol import MAVProtocol
from mavcore.messages import FenceMissionClearAll


class FenceClearProtocol(MAVProtocol):
    """
    Sends MISSION_CLEAR_ALL (mission_type = FENCE) and waits for MISSION_ACK(FENCE).
    """

    def __init__(self, target_system: int = 1, target_component: int = 0):
        super().__init__()
        self.target_system = target_system
        self.target_component = target_component

        self.clear_msg = FenceMissionClearAll(
            target_system=self.target_system,
            target_component=self.target_component,
        )

    def run(self, sender, receiver):
        sender.send_msg(self.clear_msg)
