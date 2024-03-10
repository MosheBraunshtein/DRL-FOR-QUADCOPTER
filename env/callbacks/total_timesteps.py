

from stable_baselines3.common.callbacks import BaseCallback

class Total_timesteps(BaseCallback):
    def __init__(self, verbose=0,num=0):
        super(Total_timesteps, self).__init__(verbose)
        self.total_steps = 0
        self.num = num

    def _on_step(self):
        self.total_steps += 1
        print("total steps / ", self.total_steps)
        if self.total_steps >= self.num:
            return False  # Stop training
        return True