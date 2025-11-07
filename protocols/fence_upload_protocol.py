import time
from dataclasses import dataclass
from typing import List, Tuple
from mavcore.messages.command_ack_msg import CommandAck
from pymavlink.dialects.v20 import common as mav

from mavcore.mav_protocol import MAVProtocol
from mavcore.messages import FenceMissionCount, FenceMissionItemInt


@dataclass
class FenceUploadProtocol(MAVProtocol):
    """
    Uploads polygon vertices via the Mission sub-protocol (MAV_MISSION_TYPE_FENCE).

    Handshake:
      1. MISSION_COUNT (FENCE)
      2. Repeated:
           FC -> MISSION_REQUEST_INT (FENCE, seq=i)
           Us -> MISSION_ITEM_INT (FENCE, seq=i)
      3. MISSION_ACK (FENCE)
    """

    vertices_deg: List[Tuple[float, float]]
    inclusion: bool = True  # False => EXCLUSION polygon
    target_system: int = 1
    target_component: int = 1
    handshake_timeout_s: float = 10.0
    ack_timeout_s: float = 3.0

    def __post_init__(self):
        super().__init__()
        self.ack_msg: CommandAck()

    def run(self, sender, receiver):
        n = len(self.vertices_deg)
        if n < 3:
            self.ack_msg = "ERROR: need at least 3 vertices"
            return

        # 1) Send MISSION_COUNT(FENCE)
        count_msg = FenceMissionCount(
            count=n,
            target_system=self.target_system,
            target_component=self.target_component,
        )
        sender.send_msg(count_msg)

        # 2) Serve MISSION_REQUEST_INT(FENCE) with MISSION_ITEM_INT(FENCE)
        sent = 0
        deadline = time.time() + self.handshake_timeout_s

        while sent < n and time.time() < deadline:
            req = receiver.recv_match(
                type="MISSION_REQUEST_INT", blocking=True, timeout=1.0
            )
            if not req or req.mission_type != mav.MAV_MISSION_TYPE_FENCE:
                continue

            seq = int(req.seq)
            if seq < 0 or seq >= n:
                continue

            lat, lon = self.vertices_deg[seq]

            item_msg = FenceMissionItemInt(
                seq=seq,
                lat_deg=float(lat),
                lon_deg=float(lon),
                total_vertices=n,
                inclusion=self.inclusion,
                target_system=self.target_system,
                target_component=self.target_component,
            )
            sender.send_msg(item_msg)
            sent += 1

        if sent != n:
            self.ack_msg = f"ERROR: sent {sent}/{n} fence vertices"
            return

        # 3) Wait for MISSION_ACK(FENCE)
        t0 = time.time()
        future_ack = receiver.wait_for_msg(self.ack_msg, blocking=False)
        future_ack.wait_until_finished()
