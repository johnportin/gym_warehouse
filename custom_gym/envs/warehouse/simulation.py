from envs.warehouse.components import Warehouse, Forklift, FloorPatch
import numpy as np






class Simulation:
    '''
    This sets up our Environment
    '''
    def __init__(self, X_dim, Y_dim, n_forklifts = 1, joblist_n = 100, task_n = 3):
        self.time = 0
        self.forklifts_n = n_forklifts
        self.warehouse = Warehouse(x_dim = X_dim, y_dim = Y_dim, receiving = [0,0], shipping = [X_dim - 1, Y_dim - 1], lab = [0, Y_dim - 1])
        self.forklifts = list(self.__setattr__('Forklift'+str(k), Forklift(start_position = [0,0], job = None)) for k in range(n_forklifts))

        self.task_n = task_n
        self.bucket = [[]]
        #self.jobs_n = len(self.joblist)

    def getJob(action, pos = 0):
        job = self.bucket[action][pos]
        return job

    def updateBuckets(action, pos = 0): #here, the action will be a bucket selection
        self.bucket[action].pop(pos)

    def isValid(job): ###Is there a way to clean this up?
        for forklift in self.forklifts:
            for task1 in forklift.task_list:
                for task2 in job:
                    if task1 == task2:
                        return False
        return True





    def getObs():
        #convert attributes of the class to the correct observation format
        pass
