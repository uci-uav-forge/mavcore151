import pymavlink.dialects.v20.all as dialect
from enum import Enum

from mavcore.mav_message import MAVMessage


class IntervalMessageID(Enum):
    GPS_RAW_INT = 24
    ATTITUDE = 30
    ATTITUDE_QUATERNION = 31
    LOCAL_POSITION_NED = 32
    GLOBAL_POSITION_INT = 33
    BATTERY_STATUS = 147


class RequestMessageInterval(MAVMessage):
    """
    Requests message interval stream from msg id.
    """

    def __init__(
        self, target_system: int, target_component: int, msg_id: IntervalMessageID
    ):
        super().__init__("MAV_CMD_SET_MESSAGE_INTERVAL")
        self.target_system = target_system
        self.target_component = target_component
        self.msg_id = msg_id

    def encode(self, system_id, component_id):
        return dialect.MAVLink_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=511,  # MAV_CMD_SET_MESSAGE_INTERVAL (511)
            confirmation=0,
            param1=float(self.msg_id.value),
            param2=250000.0,
            param3=0.0,
            param4=0.0,
            param5=0.0,
            param6=0.0,
            param7=1.0,
        )

    def __repr__(self):
        return f"(MAV_CMD_SET_MESSAGE_INTERVAL) timestamp: {self.timestamp}, msg_id: {self.msg_id.name}"
