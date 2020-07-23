import gym
from gym import spaces
import numpy as np
from envs.warehouse.components import Warehouse, Forklift, FloorPatch
from envs.warehouse.simulation import Simulation

TASKS_N = 1
CAPACITY = 2
LOCATIONS_N = 1
LOC1 = 0
FORKLIFTS_N = 3
JOBS_N = 100





class WarehouseEnv(gym.Env):
    def __init__(self):
        #Defines an array [length of joblist, number of forklifts, capacity of dropoff, position of forklifts x3]
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([JOBS_N, FORKLIFTS_N, CAPACITY, 100, 100, 100]), dtype = np.int)
        self.action_space = spaces.Discrete(JOBS_N * TASKS_N + 1) #+1 for wait action
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.queue = np.array([])
        self.sim = Simulation(X_dim = 5, Y_dim = 7, n_forklifts = 3)
        print('Environment initialized')






    def step(self, action = None):

        print('Step successful')

    def reset(self):
        print('Environment reset')



    def render(self):
        print(self.observation_space)
        #output = 'Completed {} jobs so far'.format(self.observation_space)
        #print(output)


    def interaction_with_ourActualEnv1():
        #update something about the environment
        pass

    #def what do with with an action
    def do_action(action):
        if action == self.action_space.n - 1: #execute wait action
            pass
        else:
            action = (action / self.sim.task_n, action % self.sim.task_n)
