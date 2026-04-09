import time
from robot.controller import UR5Controller  # Import UR5 Controller

# 1 Define UR5 connection details
UR5_IP = "192.168.140.140"  # Replace with your actual UR5 IP
PORT = 30002  # Default URScript command port

# 2 Initialize UR5 Controller
controller = UR5Controller(UR5_IP, PORT)

# 3 Test Different Motor States

print(" Motor Turning Right...")
controller.set_motor_state(True, False)  # Right Rotation
time.sleep(2)

print(" Motor Turning Left...")
controller.set_motor_state(False, True)  # Left Rotation
time.sleep(2)

print(" Motor OFF...")
controller.set_motor_state(False, False)  # OFF
time.sleep(2)

print(" Motor LOCKED (Brake Mode)...")
controller.set_motor_state(True, True)  # Locked
time.sleep(2)

print(" Test Completed. Motor control successful.")
