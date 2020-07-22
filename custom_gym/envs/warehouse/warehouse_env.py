import gym

class WarehouseEnv(gym.Env):
    def __init__(self):
        print('Environment initializaed')
    def step(self):
        print('Step successful')
    def reset(self):
        print('Environment reset')
