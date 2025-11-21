from mavcore.mav_message import MAVMessage
from mavcore.messages.attitude_msg import Attitude
from mavcore.messages.attitude_quat_msg import AttitudeQuat
from mavcore.messages.local_position_ned_msg import LocalPositionNED
from mavcore.messages.global_position_msg import GlobalPosition


class FullPose(MAVMessage):
    """
    Reads and stores full pose information from the vehicle, including:
    - Attitude (quaternion)
    - Local Position (x, y, z in NED frame and velocities)
    - Global Position (latitude, longitude, altitude)

    Contains an additonal method to get an interpolated pose at a given timestamp.
    """

    def __init__(self):
        super().__init__("FULL_POSE")
        self.attitude = AttitudeQuat()
        self.local_position = LocalPositionNED()
        self.global_position = GlobalPosition()
        self.submessages = [
            self.attitude,
            self.local_position,
            self.global_position,
        ]

    def decode(self, msg):
        if msg.get_type() == self.attitude.name:
            self.attitude.decode(msg)
        elif msg.get_type() == self.local_position.name:
            self.local_position.decode(msg)
        elif msg.get_type() == self.global_position.name:
            self.global_position.decode(msg)
        else:
            return
        self.timestamp = max(
            self.attitude.timestamp,
            self.local_position.timestamp,
            self.global_position.timestamp,
        )

    def __repr__(self) -> str:
        return f"(FULL_POSE) timestamp: {self.timestamp} ms,\n  {self.attitude}\n  {self.local_position}\n  {self.global_position}"
