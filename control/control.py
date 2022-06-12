from djitellopy import Tello 
"""
base actions:
move left n cm
move right n cm
move up n cm
move down n cm
rotate n degrees
control_motorspeeds(m1speed, m2speed, m3speed, m4speed)

"""
from pynput import keyboard

class TelloState:
    def __init__(self):
        
        self.z = 0.0
        self.x = 0.0
        self.y = 0.0

        self.x_vel = 0.0
        self.y_vel = 0.0
        self.z_vel = 0.0
  
        self.x_acc = 0.0
        self.y_acc = 0.0
        self.z_acc = 0.0

        self.pitch = 0
        self.roll = 0 
        self.yaw = 0
        self.alt = 0.0

        self.battery = 0.0
        self.time = 0.0

    def update(self, state_dict, image, info):
        """
        uses dead reconing with imu data from quad copter to interpolate position
        """
        self.image = image
        self.detections = info['detections']
        self.keypoints = info['keypoints']
        self.obstacles = info['obstacles']
        self.segmentation = info['segmentation']

        dt = state_dict['time'] - self.time
        self.x = self.x + self.x_vel*dt + self.x_acc*dt**2/2
        self.y = self.y + self.y_vel*dt + self.y_acc*dt**2/2
        self.z = self.z + self.z_vel*dt + self.z_acc*dt**2/2

        self.x_vel = state_dict['vgx']
        self.y_vel = state_dict['vgy']
        self.z_vel = state_dict['vgz']

        self.x_acc = state_dict['agx']
        self.y_acc = state_dict['agy'] 
        self.z_acc = state_dict['agz']

        self.roll = state_dict['roll']
        self.pitch = state_dict['pitch']
        self.yaw = state_dict['yaw']
        self.alt = state_dict['h']

        self.battery = state_dict['bat']
        self.time = state_dict['time']


class RLActor:
    def __init__(self, tello, agent):
        self.tello = tello
        self.agent = agent
        
    def act(self, state):
        raw_action = self.agent.act(state) #[-1,1]
        leftright_vel, frontback_vel, updown_vel, yaw_vel = int(raw_action * 100) # scale to [-100,100]
        response = self.tello.send_rc_control(leftright_vel, frontback_vel, updown_vel, yaw_vel)


class ManualController:
    def __init__(self, tello):
        self.tello = tello
        self.function_key = {
            't': self.tello.takeoff, 
            'a': self.tello.move_left,
            'd': self.tello.move_right, 
            'w': self.tello.move_forward,
            's': self.tello.move_back,
            'up': self.tello.move_up,
            "down": self.tello.move_down,
            "f": self.tello.flip_right,
            "g": self.tello.flip_left, 
            "h": self.tello.flip_forward,
            "j": self.tello.flip_back,
            #"rc": self.tello.send_rc,
            "turn right": self.tello.rotate_clockwise,
            "turn left": self.tello.rotate_clockwise,
            "go xyz speed": self.tello.go_xyz_speed, 
            "curve xyz speed": self.tello.curve_xyz_speed,
            "go xyz speed mid": self.tello.go_xyz_speed_mid,
            "curve xyz speed mid": self.tello.curve_xyz_speed_mid,
            "go xyz speed yaw mid": self.tello.go_xyz_speed_yaw_mid,
        }
        self.tello.connect()
        self.tello.takeoff()
        self.listener = keyboard.Listener(on_press=self.parse_keys)
        self.listener.start()

    def parse_keys(self, key):
        print('keyboard_command: ')
        print(key)
        print(type(key))
        print(self.function_key[str(key)])
        try:
            if not key == 't':
                arg = 10
                response = self.function_key[key](arg)
            else:
                response = self.function_key[key]()
        except:
            response = False

        return response
        
    def refresh(self,):
        #response = self.tello.send_keepalive()
        #self.listener.join()
        #self.listener.start()
        self.listener.join()
        self.listener = keyboard.Listener(on_press=self.parse_keys)
        self.listener.start()
        return None

    def print_command_map(self):
        print(self.command_map)
