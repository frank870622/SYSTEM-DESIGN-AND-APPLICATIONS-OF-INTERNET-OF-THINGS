import threading

from morse_burger_light_base64 import load_image_base64, mos_burger

import tellopy
image_list = []

def image_handler(event, sender, data):
    global image_list
    image_list.append(data)
    # publish: I'm ready take another

def take_pic_after_get_cmd(mDrone):
    """ mqtt client """
    # get cmd
    # subscribe: server_cmd
    # while listening
        # if cmd == take
            # mDrone.take_picture()
        # elif cmd == stop
            # break
    pass


def main():
    mDrone = tellopy.Tello()
    mDrone.connect()
    mDrone.subscribe(mDrone.EVENT_FILE_RECEIVED, image_handler)

    mDrone.take_picture() 

    take_pic_after_get_cmd(mDrone)

    load_image_base64(image_list)
    mos_burger()
    
    # publish answer
    # subscribe command

    mDrone.sock.sendto(b'mon', mDrone.tello_addr)
    mDrone.sock.sendto(b'mdirection 2', mDrone.tello_addr)
    mDrone.takeoff()
    mDrone.sock.sendto(bytes(final_command), mDrone.tello_addr)
    mDrone.land()


if __name__ == "__main__":
    main()


