import socket

UR5_IP = "192.168.140.140"
PORT = 30002 #URScript command port

# -----------------getting and printing current_pose + movel  (working) -----------------------#
ur_script = """
def move_linear():
    current_pose = get_actual_tcp_pose()  # Get TCP Pose

    # Open a socket connection back to Python
    socket_open("192.168.140.141", 5006)  # Change to your PC's IP and an open port

    # Send the current pose as a string
    socket_send_string(to_str(current_pose))

    # Close the socket
    socket_close()

    # Move linearly
    #target_pose = pose_trans(current_pose, p[-0.00, 0, -0.0, 0, 0, 0])  
    #movel(p[-0.720000, 0.310000, 0.410000, 0.251000, -2.090000, -2.150000], a=1)
end
move_linear()
"""

try:
    # Connect to the UR5 robot
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((UR5_IP, PORT))
        s.send(ur_script.encode('utf-8'))
        print("Command sent to UR5.")

    # Create a listening socket on the PC to receive the pose
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("192.168.140.141", 5006))  # PC's IP and port
        server.listen(1)
        print("Waiting for TCP pose data...")

        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8').strip()  # Receive pose
            print(f"Current TCP Pose: {data}")  # Print received pose

except Exception as e:
    print(f"Error: {e}")
