from robot.controller import UR5Controller
import time
from robot.movement import RobotMover
#  Initialize UR5Controller
UR5_IP = "192.168.140.140"  # Replace with your actual UR5 IP
PORT = 30002  # Default URScript communication port

controller = UR5Controller(UR5_IP, PORT)
#  Test: Send a popup message
print("\n Sending popup message...")
# controller.send_popup("hi")

#  Test: Get the current TCP pose
# print("\n Getting current TCP pose...")
tcp_pose = controller.get_current_tcp_pose()
# print(f" TCP Pose: {tcp_pose}")

#  Test: Move the robot using MoveJ
# print("\n Moving UR5 using MoveJ...")

controller.send_movel(0.0515, -0.60287, 0.199, 1.613614, -0.069675, 0.00169)

# time.sleep(1.9)
# controller.send_movel(-0.449078, -0.43089, 0.919087, 1.160916, -0.412102, -0.855129, v=0.9)
# time.sleep(1.9)
# controller.send_movel(-0.60721, 0.040256, 0.923411, 0.802024, -1.077328, -1.633504, v=0.9)
# time.sleep(1.9)
# controller.send_movel(-0.449078, -0.43089, 0.919087, 1.160916, -0.412102, -0.855129, v=0.9)
# time.sleep(1.9)
# controller.send_movel(-0.60721, 0.040256, 0.923411, 0.802024, -1.077328, -1.633504, v=0.9)
# time.sleep(1.9)
# controller.send_movel(-0.449078, -0.43089, 0.919087, 1.160916, -0.412102, -0.855129, v=0.9)
# time.sleep(1.9)








#  Test: Move the robot using MoveL
# print("\n Moving UR5 using MoveL...")








# print("\n Controller methods tested successfully!")