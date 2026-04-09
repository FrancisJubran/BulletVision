from robot.controller import UR5Controller

#  Initialize UR5Controller
UR5_IP = "192.168.140.140"  # Replace with your actual UR5 IP
PORT = 30002  # Default URScript communication port

controller = UR5Controller(UR5_IP, PORT)


#  Test: Get the current TCP pose
# print("\n Getting current TCP pose...")
tcp_pose = controller.get_current_tcp_pose()
print(f" TCP Pose: {tcp_pose}")

