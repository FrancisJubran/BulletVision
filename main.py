from camera.receiver import CameraReceiver
from robot.corrcontroller import UR5Controller

def main():
    camera = CameraReceiver("192.168.140.141", 5005)
    robot = UR5Controller("192.168.140.140", 30002)

    camera.start_listening(robot_controller=robot)

if __name__=="__main__":
    main()