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

timeout = time.time() + 10.0
while time.time() < timeout:
    pose = full_pose.get_local_position(time.time()-0.5)
    print(time.time(), pose.timestamp)
    time.sleep(0.05)
