#!/usr/bin/python3
import gymnasium as gym
import numpy as np
from env.physical_env import Sitl

class CopterGym(gym.Env):

    def __init__(self,args) -> None:
        super(CopterGym, self).__init__()

        self.args = args

        self.observation_space = gym.spaces.Dict(
            {
                "roll" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "pitch" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "yaw" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "roll_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
                "pitch_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
                "yaw_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
                "alt": gym.spaces.Box(low = 80,high = 120,shape=(1,),dtype=np.float32),
            }
        )

        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(4,),dtype=np.float32)  # Example 4 actions for throttle, roll, pitch, and yaw        

    def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''
        self.current_step += 1

        norm = lambda a: ((a + 1) * (2000-1000) / 2 + 1000)
        self.action = [norm(element) for element in action]
        assert not any(1000 > x or x > 2000 for x in self.action) , 'Env: pwm is too high or low'
        self.sitl_env.set_rc(self.action)
        
        # Receive telemetry data from the drone
        gps , attitude = self.sitl_env.get_gps_and_attitude()

        observation = self._get_obs(attitude=attitude,alt=gps.alt)

        # condition for done
        self.isCrushed = gps.alt < 2 
        self.limit = gps.alt > 101

        # Check if the episode is done
        terminated = self.isCrushed or self.limit

        reward = 0
        info = {"info" : "empty"}

        self.render(observation)

        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):
        '''
        start new episode
        '''
        self.current_step = 0

        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl(args=self.args)

        self.sitl_env.run()

        gps , attitude = self.sitl_env.get_gps_and_attitude()
        initial_observation = self._get_obs(attitude=attitude,alt=gps.alt)

        info = {"info" : "empty"}
        return initial_observation, info
    

    def render(self,obs):
        print("episode step ","/ ", self.current_step)
        print(f"""obs : 
                    roll = {obs['roll'].item()} 
                    pitch = {obs['pitch'].item()}
                    yaw = {obs['yaw'].item()}
                    roll_speed = {obs['roll_speed'].item()}
                    pitch_speed = {obs['pitch_speed'].item()}
                    yaw_speed = {obs['yaw_speed'].item()}
                    alt = {obs['alt'].item()}
            """)
        print(f"""action : 
                    roll = {self.action[0]} 
                    pitch = {self.action[1]}
                    throttle = {self.action[2]}
                    yaw = {self.action[3]}
            """)
        print("="*60)
    

    def _get_obs(self,attitude,alt):
        observation = {
            "roll": np.array([attitude.roll]).astype(np.float32),
            "pitch": np.array([attitude.pitch]).astype(np.float32),
            "yaw": np.array([attitude.yaw]).astype(np.float32),
            "roll_speed": np.array([attitude.roll_speed]).astype(np.float32),
            "pitch_speed": np.array([attitude.pitch_speed]).astype(np.float32),
            "yaw_speed": np.array([attitude.yaw_speed]).astype(np.float32),
            "alt": np.array([alt]).astype(np.float32)
        }
        return observation

    def close(self):
        '''
        close sitl process
        '''
        print("\nclose pymavlink , sim_vehicle\n")
        self.sitl_env.close()




























# class EpisodeReward(gym.Wrapper):
#     def __init__(self,env):
#         super().__init__(env)
    
#     def step(self, action):
#         copter_state,reward,terminate,truncated,info = self.env.step(action)

        

        

#         print(f"Total Reward : {reward}")

#         return copter_state,reward,terminate,truncated,info



# from gymnasium.wrappers import TimeLimit

# base_env = CopterGym()
# timeLimit_env = TimeLimit(base_env, max_episode_steps=7)
# env = EpisodeReward(timeLimit_env)


# obs,info = env.reset()
# itter = 0
# while True:
#     copter_state,reward,terminate,truncated,info = env.step([1500,1500,1000,1500])
#     print("reward", reward)
#     done = terminate or truncated
#     print("step ", itter)
#     itter += 1
#     if done:
#         print("episode end")
#         env.close()
#         break









# env_stepLimit = Wrapper(env=base_env).step

# pose,state = env_stepLimit.reset()
# print(state)
# itter = 0
# while True:
#     copter_state,reward,done,pose = env_stepLimit.env.step([1500,1500,1000,1500])
#     print(copter_state._asdict())
#     if done:
#         print("episode end")
#         break