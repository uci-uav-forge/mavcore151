from mavcore.mav_protocol import MAVProtocol
from mavcore.messages import RCOverride


class RCOverrideProtocol(MAVProtocol):
    """
    RC Override Protocol to send RC channel override commands.
    """

    def __init__(
        self,
        target_system: int = 1,
        target_component: int = 0,
        channel1=0,
        channel2=0,
        channel3=0,
        channel4=0,
        channel5=0,
        channel6=0,
        channel7=0,
        channel8=0,
        channel9=0,
        channel10=0,
        channel11=0,
        channel12=0,
        channel13=0,
        channel14=0,
        channel15=0,
        channel16=0,
        channel17=0,
        channel18=0,
    ):
        super().__init__()
        self.target_system = target_system
        self.target_component = target_component

        self.rc_override_msg = RCOverride(
            self.target_system,
            self.target_component,
            channel1=channel1,
            channel2=channel2,
            channel3=channel3,
            channel4=channel4,
            channel5=channel5,
            channel6=channel6,
            channel7=channel7,
            channel8=channel8,
            channel9=channel9,
            channel10=channel10,
            channel11=channel11,
            channel12=channel12,
            channel13=channel13,
            channel14=channel14,
            channel15=channel15,
            channel16=channel16,
            channel17=channel17,
            channel18=channel18,
        )

    def run(self, sender, receiver):
        sender.send_msg(self.rc_override_msg)
