import mavcore.mav_device as mav_device
import mavcore.messages as messages
import time

device = mav_device.MAVDevice("udp:127.0.0.1:14550")

full_pose = messages.FullPose()
device.add_listener(full_pose)

while True:
    print(full_pose)
    time.sleep(1)