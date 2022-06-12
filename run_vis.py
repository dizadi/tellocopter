
from pynput import keyboard
from control.control import ManualController
from djitellopy import Tello
import time
import cv2
from control.control import TelloState
from visualizer import UDPStreamReader, Visualizer

from perception.detect import Detector

def run_application():
    # open the window for viewing the system
    # listen for an objective 
    # call the objective the user wants 
    # when finished, hover in place or return to home
    
    
    tello = Tello()

    response = tello.connect()
    response = tello.streamon()
    #stream = cv2.VideoCapture('udp://'+'0.0.0.0'+':'+str(11111),cv2.CAP_FFMPEG) 
    detector = Detector()
    #visualizer = Visualizer(tello)
    #ret, val = stream.read()

    #while not ret:
        #ret, val = stream.read()
    i = 0
    while True:

        tello_state_dict = tello.get_current_state()
        #frame = visualizer.get_frame()
        frame = tello.get_frame_read()
        frame = frame.frame
        #print(frame)
        if i > 150:
            print("detecting")
            # run detections in a separate thread
            detections = detector.detect(frame)
        else:
            detections = False
        
        i += 1
        info = {
            "detections": detections,
            "obstacles": False, 
            "keypoints": False,
        }
        detections = info['detections']
        if detections:
            for i in range(len(detections)):
                x,y,w,h = detections['bboxes'][i]
                #color = [int(c) for c in self.colors[detections['class_ids'][i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), 'r', 2)
                #text = "{}: {:.4f}".format(self.classes[detections['class_ids'][i]], detections['confs'][i])
                #cv2.putText(frame, i, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.imshow('visualization', frame)
        cv2.waitKey(1)
        time.sleep(0.25)
        # can be speeded up with multiprocessing
        #visualizer.visualize(frame, info)
        
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