## Introduction 

This environment is based on Software In The loop (SITL) Ardupilot - 
[SITL Documentation](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html).
    
SITL simulate : flight contoller, physical modeling, dynamics, environment effects, sensors
we connect this simulation to pymavlink for get and set messages [pymavlink](https://mavlink.io/en/mavgen_python/)
we wrap this simulation in gymnasium custom environment [gymnasium](https://gymnasium.farama.org/index.html) 
and run PPO algorithm from [stable baseline](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)


     <img width="500" alt="image" src="https://github.com/MosheBraunshtein/DRL-FOR-QUADCOPTER/assets/55755575/6b063b9c-bcd5-4b92-a58f-86acdcdd3eb1">

## Installation 

### Build the Ardupilot code:
```
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
```

### Clone simondlevy/54-447-2883 to ardupilot/Tools:
```
cd ardupilot/Tools
git clone https://github.com/simondlevy/54-447-2883.git
```

### Pull image https://hub.docker.com/r/mosheee/cocpit_env:
```docker pull mosheee/cocpit_env```
    
## Run docker container

If you want to outport to another GCS (e.g gazibo,MissionPlanner) for
visualization, you need to expose port 14550 in the container and get the IP address of
the host where GCS exist.  Run folllowing command:

```docker run -it --name cocpit_drl -p 14550:14550/udp --mount type=bind,source=absolute/path/to/ardupilot,target=/ardupilot cocpit_env:latest```

```docker run -it --name sitl1 -v sitl1:/ardupilot_logs --mount type=bind,source=$("pwd"),target=/ardupilot,readonly cocpit_env:latest```

# Run environment
We're inside the container now, so navigate to relevent folder we're working on:
```cd Tools/cocpit_env/54-447-2883/drone-drl/drl/```
for training : 
```python3 train.py -total_timesteps=10```
        

## Sim parameters 

Sim parameters can be found [here](https://ardupilot.org/plane/docs/parameters.html#parameters-sim)
    
Most relevent parameters :
```
        sim_rate_hz     1200  (pixhauk controller run 400 hz)
        sim_gps_hz      10   
```
