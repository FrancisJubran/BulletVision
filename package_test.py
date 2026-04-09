from boltvision.camera.receiver import DataReceiver
from boltvision.robot.controller import UR5Controller
from boltvision.robot.movement import RobotMover

# ✅ Step 1: Initialize Components
UR5_IP = "192.168.140.140"  # Change to your actual UR5 IP
PORT = 30002  # Default UR5 script communication port

# Create UR5 Controller
controller = UR5Controller(UR5_IP, PORT)

# Create RobotMover (default reference position)
robot_mover = RobotMover(UR5_IP, PORT)

# Create DataReceiver for camera translations
receiver = DataReceiver("192.168.140.141", 5005)  # PC IP, listening to camera

print("\n Testing Methods from `corrcontroller.py`")

#  Test: Send a popup message
print(" Sending popup message...")
controller.send_popup("Hello from BoltVision!")

#  Test: Get the current TCP pose
print(" Getting current TCP pose...")
tcp_pose = controller.get_current_tcp_pose()
print(f" TCP Pose: {tcp_pose}")

#  Test: Move the robot using `send_movej`
print("\n Moving UR5 using MoveJ...")
controller.send_movej(x=-0.600, y=0.350, z=0.400, rx=0.2, ry=-2.1, rz=-2.2)

#  Test: Move the robot using `send_movel`
print("\n Moving UR5 using MoveL...")
controller.send_movel(x=-0.650, y=0.320, z=0.410, rx=0.25, ry=-2.0, rz=-2.1)

print("\n Testing Methods from `receiver.py`")

#  Test: Listen for translation data from camera
print("\n Listening for camera translation data...")
translation_data = receiver.listen(data_type="translation")
print(f" Camera Translation: {translation_data}")

print("\n Testing Methods from `movement.py`")

#  Test: Convert a camera coordinate to robot coordinate
print("\n Converting camera coordinates to robot coordinates...")
converted_coords = robot_mover.convert_camera_to_robot(
    reference_x_mm=13.0, reference_y_mm=18.0, translation_x_mm=0.2, translation_y_mm=1.0
)
print(f" Converted Robot Coordinates: {converted_coords}")

#  Test: Move robot to detected object
print("\n Moving robot to detected object using camera data...")
robot_mover.move_robot_to_detected_object(reference_x_mm=13.0, reference_y_mm=18.0)

print("\n All methods tested successfully!")
