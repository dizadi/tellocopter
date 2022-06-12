import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
 
import socket
import math
import pickle
import sys

class Visualizer:
    def __init__(self, tello):
        self.stream_reader = UDPStreamReader(host='0.0.0.0', port='11111')
        self.stream_reader.connect()
        #self.stream_reader.refresh()

    def visualize_frame(self, frame, info):
        # info should be a dictionary including:
        # detection bboxes, classes
        # initial_detection boolean for tracking
        pass

    def visualize_detection(self, frame, detection_info):
        pass
    
    def get_frame(self):
        self.stream_reader.refresh()
        return self.stream_reader.frame

    def visualize(self, image, info):
        """
        layout:
                    full frame                  : detection panel
                                SLAM Mosaiic of video              
                                Track path
        """
        frame= self.stream_reader.frame
        detections = info['detections']
        if detections:
            for i in range(len(detections)):
                x,y,w,h = detections['bboxes'][i]
                color = [int(c) for c in self.colors[detections['class_ids'][i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.classes[detections['class_ids'][i]], detections['confs'][i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        obstacles = info['obstacles']
        if obstacles:
            bigone = max(obstacles['contours'], key=cv2.contourArea) if max else None
            area = cv2.contourArea(bigone)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(bigone)
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(image, "Obstacle", (x+w/2, y-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        keypoints = info['keypoints']
        if keypoints:
            cv2.drawKeyPoints(image, keypoints)
        cv2.imshow(image, 'perception display')
        cv2.waitKey(1)#

class UDPStreamReader:
    def __init__(self, host, port):
        self.max_length = 65000
        self.host = host
        self.port = port
        self.frame = None
        self.retries = 0
        
    def connect(self):
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket.bind((self.host, self.port))
        print("-> waiting for connection")
        self.stream = cv2.VideoCapture('udp://'+self.host+':'+str(self.port),cv2.CAP_FFMPEG)
        print('Connected to UDP Stream at ', self.host,':', self.port)

    def refresh(self):  
        ret, frame = self.stream.read()
        self.frame = frame