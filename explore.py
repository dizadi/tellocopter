
from perception.detect import ObstacleDetector, Detector
from control import moves


class ObstacleState:
    def __init__(self):
        self.obstacles = []
        self.potential_openings = []

class ObstacleAvoidance:
    def __init__(self):
        self.obstacle_detector = ObstacleDetector()
    
    def step(self):
        pass

    def convert_state2action(self, obstacle_state):
        # forward towards the path with the most open area
        # turn left if no features can be defined
        # turn 
        pass



class SearchState:
    def __init__(self):
        self.ang = 0.0
        self.alt = 0.0
        self.x = 0.0
        self.y = 0.0
        self.detections = []

class Search:
    def __init__(self):
        self.detector = Detector()
        self.ang = 0.0
    
    def step(self, state):
        """
        Searches around an area
        
        looks at a spot for 5 seconds, rotate 90, look again, until 360
        detect all objects in area
        move towards the space with the least amount of detected objects
        """
        pass

    def convert_state2action(self, search_state):
        pass



class HoverState:
    def __init__(self):
        self.alt

class Hover:
    def __init__(self):
        """
        use the bottom ir camera to get as low as posisble to the ground w/out landing
        move up a little to tilt forward
        go into search mode but dont move down 
        """
        pass

    def step(self, state):
        pass
    
    def convert_state2action(self, state):
        pass
