"""
a move is a sequence of actions done ffwd to accomplish a broader motor command
each move class creates a series of actions to perform 

base actions:
move left n cm
move right n cm
move up n cm
move down n cm
rotate n degrees
control_motorspeeds(m1speed, m2speed, m3speed, m4speed)

"""

class CenterOnTrack:
    def __init__(self):
        self.target_area = None
