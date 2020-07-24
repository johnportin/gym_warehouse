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

    def step(self, action):
        reward = 0.0
        #simulation has already been updated based on the action
        '''
        for name in env.sim.forklift_names:         #loop over forklifts
            forklift = env.sim.__getattribute__(name)

            if forklift.status == '' or forklift.status == 'complete':  #take action if available forklift
                action = epsilonGreedy(epsilon)
                try:    #assign job and update environment if possible
                    forklift.task_list = env.buckets[action][0]
                    forklift.update_travel_time(time_step)
                    observation, reward, done, _ = env.step(action)
                except: #otherwise, take a negative reward
                    reward -= REWARD_BAD_SCHEDULE
        '''

        observation = self.sim.getObs()


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


    #def what do with with an action
    def do_action(self, action):
        if action == self.action_space.n - 1: #execute wait action
            pass
        else:
            action = (action / self.sim.task_n, action % self.sim.task_n) #(location, task length)
            #update the job list at location action[0] by removing a job of length action[1]

    def reward(self):
        pass

    def getObs(self):
        pass
