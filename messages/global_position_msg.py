import numpy as np
from mavcore.mav_message import MAVMessage


class GlobalPosition(MAVMessage):
    """
    Reads global position. Note altitude is in meters, speed is in meters/second, and heading is in degrees.
    """

    def __init__(self):
        super().__init__("GLOBAL_POSITION_INT")
        self.time_boot_ms = -1  # timestamp (time since system boot) in milliseconds
        self.lat = 0.0  # degrees
        self.lon = 0.0  # degrees
        self.alt_msl = 0.0  # altitude in meters, above mean sea level
        self.alt_relative = 0.0  # altitude in meters, above ground
        self.vx = 0.0  # ground x speed in m/s (positive north)
        self.vy = 0.0  # ground y speed in m/s  (positive east)
        self.vz = 0.0  # ground z speed in m/s  (positive down)
        self.heading = 0.0  # in degrees, 0.0..359.99

    def decode(self, msg):
        self.time_boot_ms = msg.time_boot_ms
        self.lat = msg.lat / 1.0e7
        self.lon = msg.lon / 1.0e7
        self.alt_msl = msg.alt / 1000.0
        self.alt_relative = msg.relative_alt / 1000.0
        self.vx = msg.vx / 100.0
        self.vy = msg.vy / 100.0
        self.vz = msg.vz / 100.0
        self.heading = msg.hdg / 100.0

    def get_pos(self):
        return np.array([self.lat, self.lon, self.alt_relative])

    def get_vel(self):
        return (self.vx, self.vy, self.vz)

    def __repr__(self) -> str:
        return f"(GLOBAL_POSITION_INT) timestamp: {self.timestamp} ms, time_since_boot {self.time_boot_ms} ms, \
            position: {self.get_pos()}, velocity: {self.get_vel()}, heading: {self.heading}"
