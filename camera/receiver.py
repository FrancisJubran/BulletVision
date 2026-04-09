import socket
import re
class DataReceiver:
    """
    A class for receiving data from the camera or UR5 robot.

    Attributes:
        host (str): The IP address of the receiving computer.
        port (int): The port number to listen for incoming data.
    """

    def __init__(self, host, port):
        """
        Initializes the DataReceiver with the provided host and port.

        Args:
            host (str): The IP address of the computer running the receiver.
            port (int): The port number for incoming data.
        """
        self.host = host
        self.port = port

    def listen(self, data_type="translation"):
        """
        Listens for incoming data and returns the parsed values.

        Args:
            data_type (str): Type of expected data
                - "translation": Returns camera shift values (x, y) for detected objects.
                - "pose": Returns UR5 TCP pose (x, y, z, rx, ry, rz).

        Returns:
            - If data_type is "translation":
                A list of tuples [(translation_x, translation_y), (tx2, ty2), ...] for multiple detected objects.
            - If data_type is "pose":
                A tuple (x, y, z, rx, ry, rz) representing the current pose of the UR5.
        """

        # Set the appropriate listening port based on the data type
        listen_port = 5005 if data_type == "translation" else 5006

        # Create a socket connection for receiving data
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(f"[DEBUG] Binding receiver to {self.host}:{listen_port}")

            # Bind the socket to the provided IP and port, then start listening for connections
            s.bind((self.host, listen_port))
            s.listen(1)
            print(f" [Receiver] Listening for {data_type} on {self.host}:{listen_port}")

            # Accept an incoming connection
            conn, addr = s.accept()
            print(f"[DEBUG] Connection established from {addr}")

            with conn:
                print(f" [Receiver] Connected from {addr}")

                # Receive data and decode it from bytes to string
                data = conn.recv(1024).decode('utf-8').strip()

                if data:
                    try:
                        if data_type == "translation":
                            """
                            Expected format: 
                            "tx1 ty1 tx2 ty2 tx3 ty3 ..." (space-separated translation values)
                            Each detected object has two values: translation_x and translation_y
                            """

                            # Expected format: ((x, y), score),((x, y), score),...
                            pattern = re.compile(r"\(\(([-\d.]+),([-\d.]+)\),[-\d.]+\)")
                            matches = pattern.findall(data)

                            if not matches:
                                print(f" [Receiver] Could not parse translation data: {data}")
                                return None

                            translation_data = [(float(x), float(y)) for x, y in matches]

                            print(f" [Receiver] Parsed Translation Data: {translation_data}")
                            return translation_data

                        elif data_type == "pose":
                            """
                            Expected format: 
                            "p[x, y, z, rx, ry, rz]"
                            The received pose represents the TCP position of the UR5.
                            """

                            print(f"[DEBUG] Raw data received: {data}")

                            # Remove unwanted characters like 'p[' and ']'
                            cleaned_data = data.replace('p[', '').replace(']', '')

                            # Convert the string into a tuple of six float values
                            pose_values = [float(val) for val in cleaned_data.split(",")]

                            # Ensure we received a valid pose with six values
                            if len(pose_values) == 6:
                                print(f" [Receiver] UR5 TCP Pose: {pose_values}")
                                return tuple(pose_values)
                            else:
                                print("️ [Receiver] Invalid pose data received.")

                    except ValueError as e:
                        print(f" [Receiver] Parsing error: {e}")

        return None  # If no data received, return None explicitly
