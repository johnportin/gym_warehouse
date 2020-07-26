import gym
from gym import spaces
import numpy as np
from envs.warehouse.components import Warehouse, Forklift, FloorPatch
from envs.warehouse.simulation import Simulation

# WAREHOUSE SETTINGS
TASKS_N = 3
JOBS_N = 30
CAPACITY = 2
LOCATIONS_N = 3
FORKLIFTS_N = 3
X_DIM = 5
Y_DIM = 5

#TRAINING SETTINGS
REWARD_BAD_SCHEDULE = -10
######FINAL_TIME = 10000

class WarehouseEnv(gym.Env):
    def __init__(self):
        #Defines an array [length of joblist, number of forklifts, capacity of dropoff, position of forklifts x3]
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([JOBS_N, FORKLIFTS_N, CAPACITY, 100, 100, 100]), dtype = np.int)
        self.action_space = spaces.Discrete(LOCATIONS_N * TASKS_N + 1) #+1 for wait action
        self.jobs_n = JOBS_N
        self.capacity = CAPACITY
        self.sim = Simulation(X_dim = X_DIM, Y_dim = Y_DIM, n_forklifts = FORKLIFTS_N)
        self.done = False
        print('Environment initialized')

    def step(self, action, time, forklift = None):
        reward = 0.0
        done = False


        if action < self.action_space.n - 1: #check to see whether the action was waiting or not
            action = self.sim.getAction(action) #return the action as a tuple for dict lookup
            print('action = {}'.format(action))
            if self.sim.isFeasible(action):
                print('action possible')
                #access the job and remove it from the job list
                job = self.sim.buckets[action][0]
                forklift.job_list = job
                forklift.job_number = 0
                self.sim.warehouse.__getattribute__(str(forklift.position)).add_forklift()
                forklift.update_pick_up_time(time)
                self.sim.buckets[action].remove(job)
                self.sim.update(time)
            else: #otherwise, take a negative reward
                print('negative reward')
                reward -= REWARD_BAD_SCHEDULE

        observation = self.sim.getObs()

        #check whether all jobs have been completed
        if sum(observation[0:TASKS_N * LOCATIONS_N]) == 0:
            print('Final observation before done = {}'.format(observation))
            done = True




        return observation, reward, done


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
