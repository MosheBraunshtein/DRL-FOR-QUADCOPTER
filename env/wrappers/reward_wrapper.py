import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/utils")

import gymnasium as gym
from calculations import spherical_law_of_cosines



class Alt_hold_wrapper(gym.Wrapper):
    def __init__(self,env):
        super().__init__(env)
    
    def step(self, action):
        copter_state,reward,terminate,truncated,info = self.env.step(action)

        reward = -10

        if terminate or truncated:
            reward = -100 if spherical_law_of_cosines(info['real_pose'],info['ref_pose']) > 5 else 0 
            self.env.close()
        
        return copter_state,reward,terminate,truncated,info