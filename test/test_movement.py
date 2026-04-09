from robot.movement import RobotMover

#  Initialize RobotMover
UR5_IP = "192.168.140.140"  # Replace with your actual UR5 IP
PORT = 30002  # Default URScript communication port

robot_mover = RobotMover(UR5_IP, PORT)

#  Test: Convert Camera Coordinates to Robot Coordinates
reference_x_mm = 13.0  # Example manually recorded X coordinate
reference_y_mm = 18.0  # Example manually recorded Y coordinate
translation_x_mm = 0.2  # Example translation from camera
translation_y_mm = 1.0  # Example translation from camera

print("\n Converting camera coordinates to robot coordinates...")
converted_coords = robot_mover.convert_camera_to_robot(
    reference_x_mm, reference_y_mm, translation_x_mm, translation_y_mm
)
print(f" Converted Robot Coordinates: {converted_coords}")

#  Test: Move Robot to Detected Object
print("\n Moving robot to detected object using camera data...")
robot_mover.move_robot_to_detected_object(reference_x_mm, reference_y_mm, z_adjustment=-0.05)

print("\n Movement methods tested successfully!")
