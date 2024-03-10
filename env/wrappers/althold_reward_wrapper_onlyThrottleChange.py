import sys
sys.path.append("/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl/utils")

import gymnasium as gym
from calculations import spherical_law_of_cosines


'''
this wrapper exist for easy way to replace credit assignment algorithems  
'''

class Alt_hold_wrapper_onlyThrottleChange(gym.Wrapper):
    def __init__(self,env):
        super().__init__(env)
    
    def step(self, action):
        
        action[0], action[1], action[3] = -1, -1, -1

        copter_state,reward,terminate,truncated,info = self.env.step(action)

        if 9 < copter_state["alt"] < 11 :
            reward = 1
        else: terminate = True     

        if terminate or truncated:
            self.env.close()
        
        return copter_state,reward,terminate,truncated,info