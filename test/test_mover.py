import time
from robot.movement import RobotMover
from robot.controller import UR5Controller
from camera.receiver import DataReceiver

#####------------------------ INITIALIZATION---------------------------------------------
# 1 Define the UR5 connection details
UR5_IP = "192.168.140.140"
PORT = 30002
controller = UR5Controller(UR5_IP, PORT)

# 2 Initialize RobotMover
robot_mover = RobotMover(
    UR5_IP, PORT,
    RO_CB3_x=0.0515, RO_CB3_y=-0.60287, RO_CB3_z=0.199,
    RO_CB3_rx=1.613614, RO_CB3_ry=-0.069675, RO_CB3_rz=0.00169,
    y_adjustment=-0.45
)

# 3 Initialize the Receiver
receiver = DataReceiver("192.168.140.141", 5005)

#####--------------------------DEFINE INPUTS-----------------------------------------------


# 4 Define goal reference points manually for each object AND origins of robot in camera's frame
RO_x_px, RO_y_px = 592, 495  # Robot's origin in camera's frame in [mm]

TAKE_IMAGE_POS = {
    "x": 0.110685, "y": -0.60287, "z": 0.203728,  # Adjust these as needed
    "rx": 1.613614, "ry": -0.069675, "rz": 0.00169
}

# ----------------------------LOOP OVER OBJECTS----------------------------------------

MAX_OBJECTS = 4  # How many objects you want to approach

for i in range(MAX_OBJECTS):
    print(f"\nMoving to take-image position for Object #{i + 1}...")
    controller.send_movel(
        TAKE_IMAGE_POS["x"], TAKE_IMAGE_POS["y"], TAKE_IMAGE_POS["z"],
        TAKE_IMAGE_POS["rx"], TAKE_IMAGE_POS["ry"], TAKE_IMAGE_POS["rz"]
    )
    time.sleep(1)

    print(f" Retrieving live camera data for Object #{i + 1}...")
    goal_live_data = receiver.listen(data_type="translation")

    if not goal_live_data or len(goal_live_data) <= i:
        print(f" No object #{i + 1} found or fewer than expected.")
        continue

    goal_x, goal_y = goal_live_data[i]

    print(f"\n Moving to RO_CB3 (Home Position) before object #{i + 1}...")
    controller.send_movel(
        robot_mover.RO_CB3_x,
        robot_mover.RO_CB3_y,
        robot_mover.RO_CB3_z,
        robot_mover.RO_CB3_rx,
        robot_mover.RO_CB3_ry,
        robot_mover.RO_CB3_rz
    )
    time.sleep(1)

    print(f" Moving to object #{i + 1} at pixel (X={goal_x}, Y={goal_y})...")
    robot_mover.move_robot_to_detected_object(
        goal_live_x_px=goal_x,
        goal_live_y_px=goal_y,
        RO_x_px=RO_x_px,
        RO_y_px=RO_y_px
    )
    time.sleep(3)
    controller.send_movel(0.3510685, -0.70287, -0.1728, 3.1, -0.069675, 0.00169, v=0.4)
    time.sleep(3)

    print(f" Done with object #{i + 1}.")

print("\n All specified objects processed successfully.")