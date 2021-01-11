from get_tello_ip import get_tello_ip
import tello
import time

def main():
    # ip = get_tello_ip()
    ip = '172.20.10.13'
    mDrone = tello.Tello(tello_ip = ip)
    
    mDrone.takePicture()
    while True:
        try:
            a = input()
            if a == 'a':
                mDrone.takePicture()
            elif a == 'b':
                mDrone.command()
                print("send command")
        except KeyboardInterrupt:
            break

    mDrone.stop()


if __name__ == "__main__":
    main()
