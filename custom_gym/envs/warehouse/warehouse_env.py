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
X_DIM = 5
Y_DIM = 5






class WarehouseEnv(gym.Env):
    def __init__(self):
        #Defines an array [length of joblist, number of forklifts, capacity of dropoff, position of forklifts x3]
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([JOBS_N, FORKLIFTS_N, CAPACITY, 100, 100, 100]), dtype = np.int)
        self.action_space = spaces.Discrete(JOBS_N * TASKS_N + 1) #+1 for wait action
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.sim = Simulation(X_dim = X_DIM, Y_dim = Y_DIM, n_forklifts = FORKLIFTS_N)
        print('Environment initialized')

    def step(self, action = None):
        reward = 0.0
        #update the simulation based on the actions
        #calculate the reward based on the action
        #calculate whether the simulation has ended (done = False)
        #return observation, reward, done, _
        print('Step successful')

    def reset(self):
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.sim = Simulation(X_dim = X_DIM, Y_dim = Y_DIM, n_forklifts = FORKLIFTS_N, joblist_n = JOBS_N, task_n = TASKS_N)

        #return observation (This will just be the initial state of the simulation)
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
            action = (action / self.sim.task_n, action % self.sim.task_n) #(location, task length)
            #update the job list at location action[0] by removing a job of length action[1]
