import sys
sys.path.append("/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl")

from env.gyms.base_env import CopterGym
from env.wrappers.althold_reward_wrapper import Alt_hold_wrapper
from env.callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-GCS_host_ip",default=None, help="use GCS or not",required=False)
parser.add_argument("-GCS_port",default=14550, help="use GCS or not",required=False)
parser.add_argument("-container_ip",default="172.17.0.2", help="docker container ip. required for establish connection with mavlink gcs",required=True)
parser.add_argument("-mav_outport",default=14551, help="for connecting two process run with the container : pymavlink, sitl")
args = parser.parse_args()

base_env = CopterGym(args)
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)

num_iter_file = 10000

model_path = f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{num_iter_file}steps"

model = PPO.load(model_path, env=timeLimit_env, print_system_info=True)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(num_iter_file):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = vec_env.step(action)
    alt = obs['alt'].item()
    if alt < 9 or alt > 11: break
print("done")