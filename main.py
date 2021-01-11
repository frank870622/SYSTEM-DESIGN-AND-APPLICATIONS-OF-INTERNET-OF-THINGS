from get_tello_ip import get_tello_ip
import tello

def main():
    ip = get_tello_ip()
    mDrone = tello.Tello(tello_ip = ip)
    mDrone.takePicture()
    mDrone.stop()


if __name__ == "__main__":
    main()
