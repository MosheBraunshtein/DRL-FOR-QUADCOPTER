import sys
sys.path.append("/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl")

from env.gyms.base_env import CopterGym
from env.wrappers.althold_reward_wrapper_onlyThrottleChange import Alt_hold_wrapper_onlyThrottleChange
from env.callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-mp_host_ip",default=None, help="mission planner GCS ip",required=False)
parser.add_argument("-mp_port",default=14550, help="mission planner GCS port",required=False)
parser.add_argument("-container_ip",default="172.17.0.2", help="docker container ip. required for establish connection with mavlink gcs")
parser.add_argument("-mav_outport",default=14551, help="for connecting two process run with the container : pymavlink, sitl")
parser.add_argument("-total_timesteps",default=40960, help="total timesteps",type=int)
parser.add_argument("-sim_hz", help="sim_hz",type=int)
parser.add_argument("-gps_hz", help="gps_hz",type=int)
parser.add_argument("-log_file_name", help="log file name")
args = parser.parse_args()

env_arg = {
    "mp_host_ip" : args.mp_host_ip,
    "mp_port" : args.mp_port,
    "container_ip" : args.container_ip,
    "mav_outport" : args.mav_outport,
    "SIM_RATE_HZ" : args.sim_hz,
    "SIM_GPS_HZ" : args.gps_hz
}

total_timesteps = args.total_timesteps



base_env = CopterGym(args=env_arg)
timeLimit_env = TimeLimit(base_env, max_episode_steps=300)
env = Alt_hold_wrapper_onlyThrottleChange(timeLimit_env)

log_folder = f"/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl/drl/trained_models/logs/ppo/alt_hold/{args.log_file_name}/{total_timesteps}_steps/"
model_zip_folder = f"/ardupilot/Tools/cocpit_env/54-447-2883/drone-drl/drl/trained_models/logs/ppo/alt_hold/{args.log_file_name}/{total_timesteps}_steps/"

# Instantiate the agent
'''
the parameters have taken from https://github.com/DLR-RM/rl-baselines3-zoo/blob/master/hyperparams/ppo.yml, MountainCarContinuous-v0 

'''
model = PPO("MultiInputPolicy",
             env,
             tensorboard_log=log_folder,
             n_steps=516,
             batch_size=32,
             gamma=0.9999,
             learning_rate=0.0000777,
             ent_coef=0.00429,
             clip_range=0.1,
             n_epochs=10,
             gae_lambda=0.9,
             max_grad_norm=5,
             vf_coef= 0.19,
             use_sde= True
             )

# Train the agent and display train total steps
callback = Total_timesteps(num=total_timesteps)

model.learn(total_timesteps=total_timesteps,callback=callback,reset_num_timesteps=False)

model.save(model_zip_folder)

print("*"*100)
print("\ntrained model folder: \n")
print(model_zip_folder)
print("\nlog folder: \n")
print(log_folder)
print("*"*100)

















# model_path = "/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_1e4steps.zip" 

# if os.path.exists(model_path):

#     model.load("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_1e4steps")

#     model.learn(total_timesteps=total_timesteps,callback=callback,reset_num_timesteps=False)

#     model.save(f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{total_timesteps}steps")

# else: assert False, "path to model is not exist"

