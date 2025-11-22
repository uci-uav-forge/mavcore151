import mavcore.mav_device as mav_device
import mavcore.messages as messages
import mavcore.protocols as protocols
import time

device = mav_device.MAVDevice("udp:127.0.0.1:14550")

full_pose = messages.FullPose()
device.add_listener(full_pose)

request_pos = protocols.RequestMessageProtocol(
            messages.IntervalMessageID.LOCAL_POSITION_NED
        )
device.run_protocol(request_pos)
request_pos = protocols.RequestMessageProtocol(
            messages.IntervalMessageID.ATTITUDE_QUATERNION
        )
device.run_protocol(request_pos)

while True:
    print(full_pose.global_position.heading)
    time.sleep(0.1)