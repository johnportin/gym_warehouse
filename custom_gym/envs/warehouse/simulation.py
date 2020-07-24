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
        self.joblist = self._generate_job_list()
        self.buckets = self._make_buckets(self._joblist_to_dict(self.joblist))
        for k in range(self.n_forklifts):
            self.__setattr__('Forklift'+str(k), Forklift(self.forklift_start_positions[k], forklift_job_lists[k]))
            self.forklift_names.append('Forklift'+str(k))
        #self.jobs_n = len(self.joblist)

    #def getJob(action, pos = 0):
    #    job = self.bucket[action][pos]
    #    return job

    #def updateBuckets(action, pos = 0): #here, the action will be a bucket selection
    #    self.bucket[action].pop(pos)

    #def isValid(job): ###Is there a way to clean this up?
    #    for forklift in self.forklifts:
    #        for task1 in forklift.task_list:
    #            for task2 in job:
    #                if task1 == task2:
    #                    return False
    #    return True





    def getObs():
        #convert attributes of the class to the correct observation format
        pass


    """
    Helper functions below
    """
    def _joblist_to_dict(self, joblist):
        """
        Turn any joblist into a dictionary.
        Key = index
        Tuple[0] = job definition
        Tuple[1] = job destination
        Tuple[3] = job length
        """
        joblist_len = len(joblist)
        job_dict={}
        for index in range(joblist_len):
            job_dict[index] = (joblist[index][0], #job definition
                               joblist[index][1], #job destination
                               len(joblist[index][0])) #job length
        return job_dict

    def _make_buckets(self, job_dict):
        """
        Turn a job info dictionary into a dictionary bucket such that:
        key = (type('Shipping' etc),job length(int))
        value = [specific jobs]
        """
        buckets = {}
        for job_key in job_dict:
            bucket_key = (job_dict[job_key][1],job_dict[job_key][2])
            try:
                buckets[bucket_key].append(job_dict[job_key][0])
            except:
                buckets[bucket_key] = [job_dict[job_key][0]]
        return buckets

    def _generate_random_job(self):
        """
        Returns a job, and the type of the job regarding its
        destination.
        """
        WAREHOUSE_DIM = self.WAREHOUSE_DIM
        RECEIVING = self.RECEIVING
        SHIPPING = self.SHIPPING
        LAB = self.LAB
        max_task_length = self.task_n

        job_length = 1 + np.random.randint(max_task_length) # number of tasks
        job = np.random.randint(WAREHOUSE_DIM, size=job_length*2)
        for i in range(0,job_length-1):
            while (job[2*i]==RECEIVING[0] and job[2*i+1]==RECEIVING[1]) or \
            (job[2*i]==SHIPPING[0] and job[2*i+1]==SHIPPING[1]) or \
            (job[2*i]==LAB[0] and job[2*i+1]==LAB[1]):
                job = np.random.randint(WAREHOUSE_DIM, size=job_length*2)
        destination = [RECEIVING, SHIPPING, LAB][np.random.choice([0,1,2])]
        if destination == RECEIVING: # if assigned receiving
            job = np.insert(job, 0, destination) # put destination in front of job
            job_type = 'Receiving'
        elif destination == SHIPPING:
            job = np.append(job, destination)
            job_type = 'Shipping'
        else:
            job = np.append(job, destination)
            job_type = 'Lab'
        job = job.reshape(job_length + 1, 2)
        return (job, job_type)

    def _generate_job_list(self):
        """
        Generate a tuple list, with each item in the list representing
        a job, and its type. List length is defined as the joblist length.
        """
        tuple_list = [self._generate_random_job() for i in range(self.joblist_n)]
        return tuple_list
