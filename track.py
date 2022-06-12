
from perception.track import Tracker
from perception.detect import Detector

from control import moves

class Track:
    def __init__(self):
        self.tracker = Tracker()

    def step(self, state):
        track_detection = self.tracker.step(state.image)
        track_state = self.convert_detection2state(track_detection)
        action = self.convert_state2action(track_state)
        return action
    
    def convert_state2action(self, track_state):
        # try to keep the detection in front of the copter
        # TODO: make a move to rotate around an object while keeping 
        #       the camera on it if its moving towards the copter
        pass

    def convert_detection2state(self, track_detection):
        pass

    def convert_pix2cm(self, delta):
        pass

    def center_on_track(self, delta): 
        pass


class KamakazeState:
    def __init__(self):
        pass

class Kamakaze:
    def __init__(self):
        """
        kamakaze towards a target
        make the detection as big as possible and dead center
        then going as fast as possible forward
        """
        pass

    def step(self):
        # use the tracker to track a target
        pass

    def convert_state2action(self, kamakaze_state):
        pass
