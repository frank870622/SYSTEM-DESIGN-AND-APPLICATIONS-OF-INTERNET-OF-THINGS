from djitellopy import Tello

print('hello')
tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(50)
tello.rotate_counter_clockwise(90)
tello.move_forward(50)

tello.land()