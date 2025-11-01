import pymavlink.dialects.v20.all as dialect
from enum import Enum
from typing import Any, Callable

from mavcore.mav_message import MAVMessage

MAV_TYPE_GCS = 6
MAV_AUTOPILOT_INVALID = 8  # Not a valid autopilot, e.g. a GCS
MAV_MODE_CUSTOM = 0
NO_FLAGS = 0


class MAVState(Enum):
    UNKNOWN = -1
    UNINITIALIZED = 0
    BOOTING_UP = 1
    CALIBRATING = 2
    STANDBY = 3
    ACTIVE = 4
    CRITICAL = 5
    EMERGENCY = 6
    POWEROFF = 7
    FLIGHT_TERMINATION = 8


class FlightMode(Enum):
    UNKNOWN = -1
    STABILIZE = 0
    ACRO = 1
    ALTHOLD = 2
    AUTO = 3
    GUIDED = 4
    LOITER = 5
    RTL = 6
    CIRCLE = 7
    LAND = 9
    DRIFT = 11
    SPORT = 13
    FLIP = 14
    AUTOTUNE = 15
    POSHOLD = 16
    BRAKE = 17
    THROW = 18
    AVOID_ADSB = 19
    GUIDED_NOGPS = 20
    SMART_RTL = 21
    FLOWHOLD = 22
    FOLLOW = 23
    ZIGZAG = 24
    SYSTEMID = 25
    HELI_AUTOROTATE = 26
    AUTO_RTL = 27
    TURTLE = 28


class Heartbeat(MAVMessage):
    """
    Heartbeat message to send and receive heartbeats.
    """

    def __init__(self, callback_func: Callable[[Any], None] = lambda x: None):
        super().__init__("HEARTBEAT", repeat_period=1.0, callback_func=callback_func)
        self.type_id = -1
        self.state = MAVState(-1)
        self.mask = 0
        self.src_sys = -1
        self.src_comp = -1
        self.mode = FlightMode(-1)

    def encode(self, system_id, component_id):
        return dialect.MAVLink_heartbeat_message(
            type=MAV_TYPE_GCS,
            autopilot=MAV_AUTOPILOT_INVALID,
            base_mode=MAV_MODE_CUSTOM,
            custom_mode=NO_FLAGS,
            system_status=MAVState.UNINITIALIZED.value,
            mavlink_version=2,
        )

    def isArmed(self) -> bool:
        return bool(self.mask >> 7)

    def decode(self, msg):
        self.type_id = msg.type
        self.state = MAVState(msg.system_status)
        self.src_sys = msg.get_srcSystem()
        self.src_comp = msg.get_srcComponent()
        self.mask = msg.base_mode
        self.mode = FlightMode(msg.custom_mode)

    def __repr__(self) -> str:
        return f"(HEARTBEAT) timestamp: {self.timestamp} ms, type: {self.type_id}, state: {self.state.name}, system: {self.src_sys}, component: {self.src_comp}"
