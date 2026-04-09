from camera.receiver import DataReceiver
from robot.controller import UR5Controller

class RobotMover:
    """
    Handles robot movement by converting camera translations to UR5-compatible positions.
    """

    def __init__(self, ip: str, port: int,
                 RO_CB3_x=-0.660631, RO_CB3_y=0.0276, RO_CB3_z=0.39500138,
                 RO_CB3_rx=-0.053216, RO_CB3_ry=-3.135838, RO_CB3_rz=-0.017059,
                 y_adjustment=-0.31):
        """
        Initializes the RobotMover with the UR5's IP, port, robot's origin (RO_CB3), and manual Y adjustment.

        Args:
            ip (str): The UR5 robot's IP address.
            port (int): The port number for URScript communication.
            RO_CB3_x (float): Robot's TCP X position in meters when at the camera's (0,0).
            RO_CB3_y (float): Robot's TCP Y position in meters (stays unchanged unless adjusted).
            RO_CB3_z (float): Robot's TCP Z position in meters when at the camera's (0,0).
            RO_CB3_rx (float): Robot's TCP RX rotation in radians.
            RO_CB3_ry (float): Robot's TCP RY rotation in radians.
            RO_CB3_rz (float): Robot's TCP RZ rotation in radians.
            y_adjustment (float): Manual calibration adjustment for Robot Y position.
        """
        self.controller = UR5Controller(ip, port)

        # Store robot's origin (RO_CB3) and calibration settings
        self.RO_CB3_x = RO_CB3_x  # X (camera X)
        self.RO_CB3_y = RO_CB3_y  # Y (robot Y, adjustable)
        self.RO_CB3_z = RO_CB3_z  # Z (camera Y)
        self.RO_CB3_rx = RO_CB3_rx
        self.RO_CB3_ry = RO_CB3_ry
        self.RO_CB3_rz = RO_CB3_rz

        # Store manual Y adjustment for calibration
        self.y_adjustment = y_adjustment

    def compute_A_final(self, goal_live_x_px: float, goal_live_y_px: float,
                        RO_x_px: float, RO_y_px: float, scale: float = 0.001, pixel_to_mm: float = 0.28993):
        """
        Computes the final robot position (X, Y, Z) based on camera input.

        Args:
            goal_live_x_px (float):  in X from the camera (px).
            goal_live_y_px (float):  in Y from the camera (px).
            RO_x_px (float): X coordinate of the robot's TCP in the camera frame (PX).
            RO_y_px (float): Y coordinate of the robot's TCP in the camera frame (PX).
            scale (float): Scale factor to convert mm to meters (default 0.001).
            pixel_to_mm (float): 0.28993 [mm/px]

        Returns:
            tuple: (final_x, final_y, final_z, rx, ry, rz) in meters & radians.
        """

        # Step 1: Compute A in pixels
        A_x_px = goal_live_x_px - RO_x_px
        A_y_px = goal_live_y_px - RO_y_px
        # Step 2: convert A to mm
        A_x_mm = A_x_px * scale * pixel_to_mm
        A_z_mm = A_y_px * scale * pixel_to_mm    # ΔZ movement (camera Y → robot Z)
        print(A_x_mm, A_z_mm)

        # Step 3: Adjust for Y-axis inversion (camera Y is downward, robot Z is upward)
        # A_z = -A_z
        print("starting to print RO_CB")
        print(self.RO_CB3_z)
        # Step 4: Compute final robot position in robot's CB3 frame
        final_x = self.RO_CB3_x - A_x_mm - 0.00  # Move in Robot X
        final_y = self.RO_CB3_y +self.y_adjustment  # Manual calibration
        final_z = self.RO_CB3_z - A_z_mm + 0.00
        print(final_x, final_y, final_z)
        return (final_x, final_y, final_z, self.RO_CB3_rx, self.RO_CB3_ry, self.RO_CB3_rz)

    def move_robot_to_detected_object(self, goal_live_x_px: float, goal_live_y_px: float,
                        RO_x_px: float, RO_y_px: float):
        """
        Moves the robot's TCP to the detected object's position using camera data.

        Args:
            goal_live_x_px (float):  in X from the camera (px).
            goal_live_y_px (float):  in Y from the camera (px).
            RO_x_px (float): X coordinate of the robot's TCP in the camera frame (PX).
            RO_y_px (float): Y coordinate of the robot's TCP in the camera frame (PX).
        """

        # Step 2: Compute final robot movement using updated function
        final_x, final_y, final_z, rx, ry, rz = self.compute_A_final(goal_live_x_px, goal_live_y_px, RO_x_px, RO_y_px)
        print(
            f" Debug: Computed MoveL command values - X: {final_x}, Y: {final_y}, Z: {final_z}, RX: {rx}, RY: {ry}, RZ: {rz}")
        # Step 3: Send Move Command
        print(f"[RobotMover] Moving to: X={final_x}, Y={final_y}, Z={final_z}")
        self.controller.send_movel(final_x, final_y, final_z, rx, ry, rz)

        print(f"Robot moved to object at ({final_x}, {final_y}, {final_z}) in meters.")
