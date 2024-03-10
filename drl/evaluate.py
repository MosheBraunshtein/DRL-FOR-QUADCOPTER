import sys
sys.path.append("/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl")

import argparse
from env.gyms.base_env import CopterGym
from env.wrappers.althold_reward_wrapper import Alt_hold_wrapper
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

parser = argparse.ArgumentParser()
parser.add_argument("-GCS_host_ip",default=None, help="use GCS or not",required=False)
parser.add_argument("-GCS_port",default=14550, help="use GCS or not",required=False)
parser.add_argument("-container_ip",default="172.17.0.2", help="docker container ip. required for establish connection with mavlink gcs",required=True)
parser.add_argument("-mav_outport",default=14551, help="for connecting two process run with the container : pymavlink, sitl")
args = parser.parse_args()

base_env = CopterGym(args=args)
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = Alt_hold_wrapper(timeLimit_env)

num_iter_file = 10000

model_path = f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{num_iter_file}steps"

model = PPO.load(model_path, env=env, print_system_info=True)


if __name__ == '__main__':

    # Evaluate the trained agent
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=2, deterministic=True)
    
    print(f"""
          
          mean_reward={mean_reward:.2f} +/- {std_reward}

        """)


