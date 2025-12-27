import pymavlink.dialects.v20.all as dialect

from mavcore.mav_message import MAVMessage, thread_safe


class RCOverride(MAVMessage):
    """
    Send RC channel override values.
    """

    def __init__(
            self, 
            target_system: int, 
            target_component: int, 
            channel1 = 0,
            channel2 = 0,
            channel3 = 0,
            channel4 = 0,
            channel5 = 0,
            channel6 = 0,
            channel7 = 0,
            channel8 = 0,
            channel9 = 0,
            channel10 = 0,
            channel11 = 0,
            channel12 = 0,
            channel13 = 0,
            channel14 = 0,
            channel15 = 0,
            channel16 = 0,
            channel17 = 0,
            channel18 = 0
            ):
        super().__init__("RC_CHANNELS_OVERRIDE")
        self.target_system = target_system
        self.target_component = target_component
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.channel5 = channel5
        self.channel6 = channel6
        self.channel7 = channel7
        self.channel8 = channel8
        self.channel9 = channel9
        self.channel10 = channel10
        self.channel11 = channel11
        self.channel12 = channel12
        self.channel13 = channel13
        self.channel14 = channel14
        self.channel15 = channel15
        self.channel16 = channel16
        self.channel17 = channel17
        self.channel18 = channel18

    def encode(self, system_id, component_id):
        return dialect.MAVLink_rc_channels_override_message(
            target_system=self.target_system,
            target_component=self.target_component,
            chan1_raw=self.channel1,
            chan2_raw=self.channel2,
            chan3_raw=self.channel3,
            chan4_raw=self.channel4,
            chan5_raw=self.channel5,
            chan6_raw=self.channel6,
            chan7_raw=self.channel7,
            chan8_raw=self.channel8,
            chan9_raw=self.channel9,
            chan10_raw=self.channel10,
            chan11_raw=self.channel11,
            chan12_raw=self.channel12,
            chan13_raw=self.channel13,
            chan14_raw=self.channel14,
            chan15_raw=self.channel15,
            chan16_raw=self.channel16,
            chan17_raw=self.channel17,
            chan18_raw=self.channel18
        )

    @thread_safe
    def __repr__(self):
        return f"(RC_CHANNELS_OVERRIDE) timestamp: {self.timestamp}, channel1: {self.channel1}, channel2: {self.channel2}, channel3: {self.channel3}, channel4: {self.channel4}, channel5: {self.channel5}, channel6: {self.channel6}, channel7: {self.channel7}, channel8: {self.channel8}, channel9: {self.channel9}, channel10: {self.channel10}, channel11: {self.channel11}, channel12: {self.channel12}, channel13: {self.channel13}, channel14: {self.channel14}, channel15: {self.channel15}, channel16: {self.channel16}, channel17: {self.channel17}, channel18: {self.channel18}"
