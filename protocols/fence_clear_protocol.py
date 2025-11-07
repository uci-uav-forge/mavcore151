import time
from dataclasses import dataclass
from pymavlink.dialects.v20 import common as mav

from mavcore.mav_protocol import MAVProtocol
from mavcore.messages import FenceMissionClearAll


@dataclass
class FenceClearProtocol(MAVProtocol):
    """
    Sends MISSION_CLEAR_ALL (mission_type = FENCE) and waits for MISSION_ACK(FENCE).
    """

    target_system: int = 1
    target_component: int = 1
    timeout_s: float = 3.0

    def __post_init__(self):
        super().__init__()
        self.ack_msg: str | None = None
        self._clear_msg = FenceMissionClearAll(
            target_system=self.target_system,
            target_component=self.target_component,
        )

    def run(self, sender, receiver):
        # Send clear via MAVCore message wrapper
        sender.send_msg(self._clear_msg)

        # Wait for MISSION_ACK(FENCE)
        t0 = time.time()
        while time.time() - t0 < self.timeout_s:
            ack = receiver.recv_match(type="MISSION_ACK", blocking=False)
            if ack and getattr(ack, "mission_type", 0) == mav.MAV_MISSION_TYPE_FENCE:
                self.ack_msg = f"MISSION_ACK(FENCE): {ack.type}"
                return

        self.ack_msg = "TIMEOUT waiting for MISSION_ACK(FENCE)"
