import socket
import time

from camera.receiver import DataReceiver


class UR5Controller:
    """
     A controller class for managing UR5 communication using URScript commands.

     Attributes:
        ip (str): The IP address of the UR5 robot.
        port (int): The communication port (default: 300002).
    """
    def __init__(self, ip, port=30002):
        """
            Initializes the UR5 Controller with IP and port.

            Args:
                ip (str): The IP address of the UR5 robot.
                port (int, optional): The port number for URScript communication. Default is 30002.
        """
        self.ip = ip
        self.port = port

    def send_urscript(self, script: str, description: str = "Command"):
        """
        Sends a URscript command to the UR5 robot.

        Args:
            script (str): The URScript command as a string.
            description (str, optional): A short description for logging purposes. Default is "command".
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ip, self.port)) # Establish connection to the UR5
                s.sendall(script.encode('utf-8')) # Send the URScript command
                print(f"[UR5] {description} sent successfully.")
        except Exception as e:
            print(f"[UR5] Error sending {description}: {e}")

    def send_popup(self, message):
        """
        Displays a popup message on the UR5 Polyscope screen.

        Args:
            message (str): The text to display in the popup window.
        """
        ur_script = f'''
    def show_message():
        popup("{message}", title="BoltVision Message", blocking=False)
    end
    show_message()
'''
        self.send_urscript(ur_script, "Popup Message")

    def send_movej(self, x: float, y: float, z: float, rx: float = None, ry: float = None, rz: float = None,
                   a: float = 2, v: float = 0.5):
        """
        Moves the UR5 robot to a target position using MoveJ.
        Linear Variation in join Angles
        Non-Linear Variation in End-Effector position


        Args:
            x (float): X-coordinate in meters.
            y (float): Y-coordinate in meters.
            z (float): Z-coordinate in meters.
            rx (float, optional): Rotation around X-axis in radians. Default is None (UR5 decides best angle).
            ry (float, optional): Rotation around y-axis in radians. Default is None (UR5 decides best angle).
            rz (float, optional): Rotation around z-axis in radians. Default is None (UR5 decides best angle).
            a (float, optional): Acceleration value. Default is 1.
            v (float, optional) Velocity value. Default is 0.04.
        """

        # if any rotation value is None, get the current pose
        if None in (rx, ry, rz):
            current_pose = self.get_current_tcp_pose()
            if current_pose:
                rx = rx if rx is not None else current_pose[3]
                ry = ry if ry is not None else current_pose[4]
                rz = rz if rz is not None else current_pose[5]

        # format rotation values properly

        rotation_str = ', '.join(str(val) for val in (rx, ry, rz))

        ur_command = f'''
def cam_move():
    popup("Moving to X={x}, Y={y}, Z={z}", title="Moving", blocking=False)
    movej(p[{x}, {y}, {z}, {rotation_str}], a={a}, v={v})
end
cam_move()
'''
        self.send_urscript(ur_command, "MoveJ Command")

    def send_movel(self, x: float, y: float, z: float, rx: float = 0, ry: float = 0, rz: float = 0,
                   a: float = 1, v: float = 0.4):
        """ Move the UR5 in a straight line (movel)
        Non-Linear Variation in Join Angles
        Linear Variation in End-Effector position

        Args:
            x (float): X-coordinate in meters.
            y (float): Y-coordinate in meters.
            z (float): Z-coordinate in meters.
            rx (float, optional): Rotation around X-axis in radians. Default is None (UR5 decides best angle).
            ry (float, optional): Rotation around y-axis in radians. Default is None (UR5 decides best angle).
            rz (float, optional): Rotation around z-axis in radians. Default is None (UR5 decides best angle).
            a (float, optional): Acceleration value. Default is 1.
            v (float, optional) Velocity value. Default is 0.04.
        """
        # If any rotation value is None, get the current pose
        if None in (rx, ry, rz):
            current_pose = self.get_current_tcp_pose()
            if current_pose:
                rx = rx if rx is not None else current_pose[3]
                ry = ry if ry is not None else current_pose[4]
                rz = rz if rz is not None else current_pose[5]

        # Format rotation values properly
        rotation_str = ', '.join(str(val) for val in (rx, ry, rz))
        ur_command = f'''
def move_linear():
    movel(p[{x}, {y}, {z}, {rotation_str}], a={a}, v={v})
end
move_linear()
'''
        self.send_urscript(ur_command, "MoveL Command")

    def get_current_tcp_pose(self):
        """
        Retrieves the current TCP pose (position & orientation) of the UR5.

        Returns:
            tuple: (x, y, z, rx, ry, rz) in meters and radians, or None if retrieval fails.
        """
        ur_script = '''
def get_current_pose():
    current_pose = get_actual_tcp_pose()
    socket_open("192.168.140.141", 5006)  #  PC's IP

    # Send the current pose as a string
    socket_send_string(to_str(current_pose))

    # Close the socket
    socket_close()
end
get_current_pose()
'''

        # Send URScript to UR5
        self.send_urscript(ur_script, "Get Current Pose")

        # Use DataReceiver to listen for the response
        receiver = DataReceiver("192.168.140.141", 5006)
        pose = receiver.listen(data_type="pose")

        if pose:
            print(f" Current TCP Pose: {pose}")
            return pose
        else:
            print(" Failed to retrieve TCP pose")
            return None

    def set_motor_state(self, do8: bool, do9: bool):
        """
        Controls the double relay connected to DO0 and DO1.

        Args:
            do0 (bool): State of Digital Output 0 (True = ON, False = OFF)
            do1 (bool): State of Digital Output 1 (True = ON, False = OFF)
        """
        ur_script = f'''
    def control_motor():
        set_tool_digital_out(8, {str(do8).lower()})  # Set DO0
        set_tool_digital_out(9, {str(do9).lower()})  # Set DO1
    end
    control_motor()
    '''
        # Send URScript to UR5
        self.send_urscript(ur_script, f"Set Motor State: DO8={do8}, DO9={do9}")
