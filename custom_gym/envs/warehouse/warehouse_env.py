import gym
from gym import spaces
import numpy as np

TASKS_N = 1
CAPACITY = 2
LOCATIONS_N = 1
LOC1 = 0
FORKLIFTS_N = 3
JOBS_N = 100


# @hansen This function should be included in WarehouseEnv, but it doesn't seem to like that. why?
def createJobList(list_length, task_length):
    arr = np.array([np.array([np.random.randint(0,100) for j in range(task_length)]) for j in range(list_length)])
    return arr

class WarehouseEnv(gym.Env):
    def __init__(self):
        #Defines an array [length of joblist, number of forklifts, capacity of dropoff, position of forklifts x3]
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([JOBS_N, FORKLIFTS_N, CAPACITY, 100, 100, 100]), dtype = np.int)
        self.action_space = spaces.Discrete(JOBS_N * TASKS_N + 1) #+1 for wait action
        self.jobs_n = JOBS_N
        self.joblist = createJobList(JOBS_N, TASKS_N)
        self.forklifts_n = FORKLIFTS_N
        self.capacity = CAPACITY
        self.queue = np.array([])
        print('Environment initialized')




    def step(self, action = None):

        print('Step successful')

    def reset(self):
        print('Environment reset')



    def render(self):
        print(self.observation_space)
        #output = 'Completed {} jobs so far'.format(self.observation_space)
        #print(output)
