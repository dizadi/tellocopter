from detect import Detector
import cv2

class Tracker:
    def __init__(self, id, detector):
        self.detector = detector
        self.id = id
        self.initial_detection = None
        self.default_expand = 50

    def get_initial_detection(self, frame):
        # look in the entire frame for the detection
        detections = self.detector.detect(frame)
        for d in detections:
            if d['id'] == self.id:
                self.initial_detection = d
                return d

    def track_object(self, frame):
        def dist(x,y,x1,y1):
            return ((new_y - y)**2 + (new_x-x)**2)**0.5

        frame = self.crop_track_frame(frame, expand = self.default_expand)
        detections = self.detector.detect(frame)
        new_x = self.y
        new_y = self.x
        min_dist = 1e6

        track_detection = None
        for d in detections:
            x, y = self.map_detection_centers_from_track_frame(d['bbox'])
            if dist(x,y,new_x, new_y) <= min_dist:
                track_detection = d

        if track_detection is None:
            track_detection = self.get_initial_detection(frame)
        
        return track_detection

    def step(self, frame):
        if self.initial_detection:
            # crop the frame around the current detection +N pixels in every direction
            # use the detector on the cropped frame to find the object in the next location
            # map the detector location bck to the original frame location
            # use the new location to send an action based on the starting distance 
            track_detection = self.track_object(frame)
        else:
            track_detection = self.get_initial_detection(frame)
            # let the user choose which detection to track?
        
        action = self.map_detection_to_action(self, track_detection)

        return action

    def map_detection_to_action(self,detection):
        # map the current detection location to an action for the uav
        # try to keep the detection in the center of the frame at the same size as initialized
        # if the detection is None, begin to "search around" and look for the detection again, then track
        pass
    
    def crop_track_frame(self, frame, expand):
        # crop the frame around the last frame detection location given the expand size
        pass
    
    def map_detection_centers_from_track_frame(self, ):
        pass

class KeypointAssociator:
    def __init__(self):
        self.last_keypoints =[]
        self.last_descriptors = []
        self.matcher = cv2.BFMatcher()

    def step(self, kpts, descriptors):
        order = self.matcher.match(last_descriptors, descriptors)
        associations = order[:100]
        return associations