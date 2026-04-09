from camera.receiver import DataReceiver

#  Initialize DataReceiver
receiver = DataReceiver("192.168.140.141", 5005)  # Replace with your actual IP and port

#  Test: Listen for translation data (camera)
print("\n Listening for camera translation data...")
translation_data = receiver.listen(data_type="translation")
print(f" Translation Data Received: {translation_data}")

# #  Test: Listen for pose data (UR5 TCP pose)
# print("\n Listening for UR5 TCP pose data...")
pose_data = receiver.listen(data_type="pose")
# print(f" UR5 Pose Data Received: {pose_data}")
#
# print("\n Receiver methods tested successfully!")
