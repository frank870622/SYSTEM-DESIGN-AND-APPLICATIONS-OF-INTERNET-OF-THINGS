import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamon()


frame_read = tello.get_frame_read()
cv2.imshow("picture.png", frame_read.frame)


tello.takeoff()


tello.land()