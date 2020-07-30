import gym
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt
from envs.warehouse.components import Warehouse, Forklift, FloorPatch
from envs.warehouse.simulation import Simulation

# WAREHOUSE SETTINGS
TASKS_N = 3
JOBS_N = 100
CAPACITY = 3
LOCATIONS_N = 3
FORKLIFTS_N = 15
X_DIM = 10
Y_DIM = 10
FINAL_TIME = 700

#TRAINING SETTINGS
#@REWARD_BAD_SCHEDULE = -10
######FINAL_TIME = 10000

class WarehouseEnv(gym.Env):
    def __init__(self):
        #Defines an array [length of joblist, number of forklifts, capacity of dropoff, position of forklifts x3]
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([JOBS_N, FORKLIFTS_N, CAPACITY, 100, 100, 100]), dtype = np.int)
        self.action_space = spaces.Discrete(LOCATIONS_N * TASKS_N + 1) #+1 for wait action
        self.max_time = FINAL_TIME
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.sim = Simulation(X_dim = X_DIM, Y_dim = Y_DIM, n_forklifts = FORKLIFTS_N, joblist_n = JOBS_N)
        self.done = False
        print('Environment initialized')

    def step(self, action, time, forklift = None):
        reward = 0.0
        done = False

        if action < self.action_space.n - 1: #check to see whether the action was waiting or not
            action = self.sim.getAction(action) #return the action as a tuple for dict lookup
            #print('action = {}'.format(action))
            if self.sim.isFeasible(action):
                #print('action possible')
                #access the job and remove it from the job list
                job = self.sim.buckets[action][0]
                forklift.job_list = job
                forklift.job_number = 0
                self.sim.warehouse.__getattribute__(str(forklift.position)).add_forklift()
                forklift.update_pick_up_time(time)
                self.sim.buckets[action].remove(job)
                self.sim.update(time)

            reward = self.reward(time)
        else: #action == self.action_space.n - 1:
            observation = self.sim.getObs()
            if time == self.max_time -1:
                reward = self.reward(time)
            else:
                for i in range(9, 12):
                    if observation[i] < self.capacity:
                        reward = -1


        observation = self.sim.getObs()
        #check whether all jobs have been completed
        if sum(observation[0:TASKS_N * LOCATIONS_N]) == 0:
            #print('Final observation before done = {}'.format(observation))
            done = True

        #since a forklift was given, we have an availabilty
        observation[-1] = 1 #set last value to 1, else 0

        return observation, reward, done

    def reward(self, time): #reward for end of episode
        observation = self.sim.getObs()
        penalty = 0.0
        reward = 0.0

        if sum(observation[0:9]) == 0 or time == self.max_time-1:
            for i in range(0,9):
                penalty += observation[i]
            reward = 5 * self.max_time / 100 * ( 1 - (penalty / (self.jobs_n)))  #penalize if jobs left over
        #elif observation[-1] == 1: #only penalize if an action could have been taken
        #    reward = -1
        elif time > 0.8 * self.max_time:
            reward = -0.01 * max(time - 0.8 * self.max_time, 0)

        return reward

    def reset(self):
        '''Resets the environment for another run
            returns the initial state'''
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.sim = Simulation(X_dim = X_DIM, Y_dim = Y_DIM, n_forklifts = FORKLIFTS_N, joblist_n = JOBS_N, task_n = TASKS_N)
        #print('Environment reset')
        return self.sim.getObs()
        #return observation (This will just be the initial state of the simulation)

    def render(self):
        #print(self.observation_space)
        #output = 'Completed {} jobs so far'.format(self.observation_space)
        #print(output)
        pass
