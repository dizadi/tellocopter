
from pynput import keyboard
from control.control import ManualController
from djitellopy import Tello
import time
import cv2
from control.control import TelloState
from visualizer import UDPStreamReader, Visualizer

from perception.detect import Detector
from pynput import keyboard

def writekey(key):
    print(key)
def run_application():
    # open the window for viewing the system
    # listen for an objective 
    # call the objective the user wants 
    # when finished, hover in place or return to home
    
    
    tello = Tello()
    tello_state = TelloState()

    #response = tello.connect()
    controller = ManualController(tello)

    while True:
        time.sleep(1)
        controller.refresh()
    

        """ to be moved to actor class
        command = input('enter a valid command')
        if command == "flip right":
            response = tello.flip_right()
        elif command == "forward":
            response = tello.move_forward(20)
        elif command  == "back":
            response = tello.move_back(20)
        elif command == "right":
            tello.move_right(20)
        elif command == 'left':
            tello.move_left(20)
        elif command == "spin":
            response = tello.rotate_clockwise(90)
        elif command == "take off":
            response = tello.takeoff()
        elif command == "land":
            response = tello.land()

        elif command  == "end":
            response = tello.land()
            break
        
        else:
            response = tello.send_keepalive()
        """

run_application()