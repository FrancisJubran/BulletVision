import socket

ROBOT_IP = "192.168.140.140"  # Change to your UR5's IP address
PORT = 30002  # UR5 URScript port

script = """
def trigger_tool_outputs():
    set_tool_digital_out(0, True)
    sleep(2)
    set_tool_digital_out(0, False)

    set_tool_digital_out(1, True)
    sleep(2)
    set_tool_digital_out(1, False)

trigger_tool_outputs()
"""

# Open a socket connection to the UR5 robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ROBOT_IP, PORT))
sock.send(script.encode())
sock.close()
