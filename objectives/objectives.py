

"""
Objectives are broad commands for the copter to autonomously accomplish using feedback from the copter

Objectives can include 
tracking an object over time
doing a flip
doing a torpedo towards a target
obstacle avoidance with camera and IR sensors bottom 

actions:
move left n cm
move right n cm
move up n cm
move down n cm
rotate n degrees
control_motorspeeds(m1speed, m2speed, m3speed, m4speed)

"""

from . import explore
from . import track

