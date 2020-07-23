from envs.warehouse.components import Warehouse, Forklift, FloorPatch
import numpy as np


    # @hansen This function should be included in WarehouseEnv, but it doesn't seem to like that. why?
def createJobList(list_length = 100, job_length = 3):
    arr = np.array([np.array([np.random.randint(0,100) for j in range(np.random.randint(1, job_length+1))]) for j in range(list_length)], dtype = object)
    return arr

class Simulation:
    '''
    This sets up our Environment
    '''
    def __init__(self, X_dim, Y_dim, n_forklifts = 1, joblist_n = 100, task_n = 3):
        self.time = 0
        self.forklifts_n = n_forklifts
        self.warehouse = Warehouse(x_dim = X_dim, y_dim = Y_dim, receiving = [0,0], shipping = [X_dim - 1, Y_dim - 1], lab = [0, Y_dim - 1])
        self.forklifts = list(self.__setattr__('Forklift'+str(k), Forklift(start_position = [0,0], job_list = None)) for k in range(n_forklifts))

        self.task_n = task_n
        self.joblist = createJobList()
        self.jobs_n = len(self.joblist)
