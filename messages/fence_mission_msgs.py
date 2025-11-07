from dataclasses import dataclass
from pymavlink.dialects.v20 import common as mav


@dataclass
class FenceMissionClearAll:
    """
    Wrapper for MISSION_CLEAR_ALL (mission_type = FENCE).
    """

    target_system: int = 1
    target_component: int = 1

    def to_mavlink(self) -> mav.MAVLink_mission_clear_all_message:
        return mav.MAVLink_mission_clear_all_message(
            target_system=self.target_system,
            target_component=self.target_component,
            mission_type=mav.MAV_MISSION_TYPE_FENCE,
        )


@dataclass
class FenceMissionCount:
    """
    Wrapper for MISSION_COUNT (mission_type = FENCE).
    """

    count: int
    target_system: int = 1
    target_component: int = 1

    def to_mavlink(self) -> mav.MAVLink_mission_count_message:
        return mav.MAVLink_mission_count_message(
            target_system=self.target_system,
            target_component=self.target_component,
            count=self.count,
            mission_type=mav.MAV_MISSION_TYPE_FENCE,
        )


@dataclass
class FenceMissionItemInt:
    """
    Wrapper for MISSION_ITEM_INT (mission_type = FENCE) for a single polygon vertex.
    """

    seq: int
    lat_deg: float
    lon_deg: float
    total_vertices: int
    inclusion: bool = True  # False => exclusion polygon
    target_system: int = 1
    target_component: int = 1

    def to_mavlink(self) -> mav.MAVLink_mission_item_int_message:
        command = (
            mav.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
            if self.inclusion
            else mav.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION
        )

        return mav.MAVLink_mission_item_int_message(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=self.seq,
            frame=mav.MAV_FRAME_GLOBAL,
            command=command,
            current=0,
            autocontinue=0,
            param1=float(self.total_vertices),
            param2=0.0,
            param3=0.0,
            param4=0.0,
            x=int(self.lat_deg * 1e7),
            y=int(self.lon_deg * 1e7),
            z=0.0,
            mission_type=mav.MAV_MISSION_TYPE_FENCE,
        )
