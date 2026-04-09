import socket
# #-------------get x,y (translations), working----------------
# HOST = "192.168.140.141"  # Your PC IP
# PORT = 5005               # Port you configured on camera
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(1)
#     print(f"Listening clearly on {HOST}:{PORT}")
#
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         data = conn.recv(1024)
#         if data:
#             result_string = data.decode('utf-8').strip()
#             print("Camera result:", result_string)
#
#             x_str, y_str = result_string.split('-')
#             x, y = float(x_str), float(y_str)
#             print(f"Extracted: X={x}, Y={y}")
#
#


# ------------------ this is working linear move---------------------------
# ur_script = """
# def move_linear():
#     current_pose = get_actual_tcp_pose()
#     target_pose = pose_trans(current_pose, p[-0.002, 0, 0.0, 0, 0, 0])  # Move X=300mm, Y=200mm, Z=150mm
#     movel(target_pose, a=1)
# end
# move_linear()
# """
#
# try:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((UR5_IP, PORT))
#         s.send(ur_script.encode('utf-8'))
#         print("✅ Moving in X, Y, Z using movel()")
# except Exception as e:
#     print(f"❌ Error: {e}")


UR5_IP = "192.168.140.140"
PORT = 30002 #URScript command port

# -----------------getting and printing current_pose + movel  (working) -----------------------#
ur_script = """
def move_linear():
    current_pose = get_actual_tcp_pose()  # Get TCP Pose

    # Open a socket connection back to Python
    socket_open("192.168.140.141", 5005)  # Change to your PC's IP and an open port

    # Send the current pose as a string
    socket_send_string(to_str(current_pose))

    # Close the socket
    socket_close()

    # Move linearly
    target_pose = pose_trans(current_pose, p[-0.00, 0, -0.0, 0, 0, 0])  
    movel(p[-0.720831, 0.313466, 0.408736, 0.251116, -2.090886, -2.153699], a=1)
end
move_linear()
"""

try:
    # Connect to the UR5 robot
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((UR5_IP, PORT))
        s.send(ur_script.encode('utf-8'))
        print("✅ Command sent to UR5.")

    # Create a listening socket on the PC to receive the pose
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("192.168.140.141", 5005))  # PC's IP and port
        server.listen(1)
        print("🔄 Waiting for TCP pose data...")

        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8').strip()  # Receive pose
            print(f"📍 Current TCP Pose: {data}")  # Print received pose

except Exception as e:
    print(f"❌ Error: {e}")