from envs.warehouse.components import Warehouse, Forklift, FloorPatch
import numpy as np

class Simulation:
    '''
    This sets up our Environment
    '''
    def __init__(self, X_dim, Y_dim, n_forklifts = 1, joblist_n = 100, task_n = 3):
        self.WAREHOUSE_DIM = X_dim
        self.LAB = [0, Y_dim - 1]
        self.SHIPPING = [X_dim - 1, Y_dim - 1]
        self.RECEIVING = [0,0]

        self.forklifts_n = n_forklifts
        self.warehouse = Warehouse(x_dim = X_dim, y_dim = Y_dim, receiving = [0,0], shipping = [X_dim - 1, Y_dim - 1], lab = [0, Y_dim - 1])
        self.locations_n = 3
        #self.forklifts = list(self.__setattr__('Forklift'+str(k), Forklift(start_position = [0,0], job = None)) for k in range(n_forklifts))

        self.jobs_n = joblist_n
        self.task_n = task_n
        self.joblist = self._generate_job_list()
        self.buckets = self._make_buckets(self._joblist_to_dict(self.joblist))

        self.forklift_names = []
        for k in range(self.forklifts_n):
            self.__setattr__('Forklift'+str(k), Forklift([0,0], []))
            self.forklift_names.append('Forklift'+str(k))

    def getJobType(self, job):
        locations = [self.SHIPPING, self.LAB, self.RECEIVING]
        #print('job = ', job)
        if len(job) > 0:
            #print('looking for the job')
            for task in job:
                for i in range(len(locations)):
                    #print('{}, {}, types {} and {}'.format(task, locations[i], type(task), type(locations[i])))
                    if list(task) == locations[i]:
                        return i
        else:
            return None

    def getCapacity(self):
        capacities = np.zeros(3)
        '''
            loop over all forklifts and update capacity based on how many
            forklifts are currently assigned to that location
        '''

        for name in self.forklift_names:         #loop over forklifts
            forklift = self.__getattribute__(name)
            job = forklift.job_list
            #print('getCapacity(): job = ', forklift.job_list)
            try:
                index = self.getJobType(job)
                if capacities[index] < 3:
                    capacities[index] += 1
            except:
                continue
            #print('job type = {}'.format(index))


            #print('cap = {}'.format(capacities))

        return capacities

        '''     def toGrad(self, obs): #converts
        gradient = [0, self.jobs_n / (self.task_n * 3 * 2), self.jobs_n / self.task_n]
        if obs <= 0:
            obs = 0
        elif obs > 0 and obs <= gradient[1]:
            obs = 1
        elif obs > gradient[1] and obs < gradient[2]:
            obs = 2
        else:
            obs = 3
        return obs'''


    def toGrad(self, obs):  #More memory efficient
        gradient = [0, self.jobs_n / (self.task_n * 3 * 2), self.jobs_n / self.task_n]
        if obs <= 0:
            obs = 0
        elif obs > 0 and obs <= gradient[1]:
            obs = 1
        else:
            obs = 2
        return obs
    
    def toGradNoLength(self, obs):  #More memory efficient
        """
        The gradient fuction that deals with the observation spaces with no specific task lengths
        """
        gradient = [0, self.jobs_n / (self.task_n * 3 * 2), self.jobs_n / self.task_n]
        if obs <= 0:
            obs = 0
        elif obs > 0 and obs <= gradient[1]:
            obs = 1
        else:
            obs = 2
        return obs

    def getObs(self):
        """
        Observation vector: 
        (Num of forklifts at Shipping, (could be rescaled or not)
        Num of forklifts at Lab,
        Num of forklifts at Receiving,
        Capacity at Shipping,
        Capacity at Lab,
        Capacity at Receiving,
        Whether there is a forklift available)
        """
        observation = np.zeros(7) # see above
        #observation = np.zeros((self.task_n + 1) * 3 + 1) #each (loc, tasklength) pair + capacity of each location (These are set to 3?) + 1 (I forgot, it doesn't get updated)
        locations = ['Shipping', 'Lab', 'Receiving']

        for i in range(len(locations)): #update number of jobs left of each type
            observation[i] = self.toGradNoLength(len(self.buckets[locations[i]]))
            #for tsk_len in range(self.task_n):
                #observation[3*i+tsk_len] = self.toGrad(len(self.buckets[(locations[i], tsk_len+2)]))

        capacities = self.getCapacity() #grab capacities and update observation
        #start_cap = self.task_n*3
        for i in range(3):
            observation[3+i] = capacities[i]

        return observation


    def getAction(self, action):
        locations = ['Shipping', 'Lab', 'Receiving']
        x = action / self.locations_n
        y = action % self.task_n
        x, y = int(x), int(y) #cast to integers
        action = (locations[x], y+2)
        return action



    def isFeasible(self, action):
        try:

            #print(self.buckets[action][0])
            self.buckets[action][0]
            #print('is feasible')
            return True
        except:
            return False

    def update(self, time):   #updates the simulation, does not update time
        #loop through all forklifts and update their status
        for name in self.forklift_names:
            forklift = self.__getattribute__(name)

            #updates a forklift if its time has come
            if forklift.next_update_time <= time:
                #if next location is unoccupied, add this forklift to it and update the next time
                if forklift.status == 'traveling' or forklift.status == 'waiting':
                    if self.warehouse.__getattribute__(str(forklift.position)).occupied == 0:
                        #print('adding forklif to {}'.format(forklift.position))
                        self.warehouse.__getattribute__(str(forklift.position)).add_forklift()
                        forklift.update_pick_up_time(time)
                    else:
                        forklift.status = 'waiting'
                #if it was picking, update its status to next position
                elif forklift.status == 'picking':
                    #print('removing forklift at {}'.format(forklift.position))
                    self.warehouse.__getattribute__(str(forklift.position)).remove_forklift()
                    forklift.update_travel_time(time)

    """
    Helper functions below
    """
    def _joblist_to_dict(self, joblist):
        """
        Turn any joblist into a dictionary.
        Key = index
        Tuple[0] = job definition
        Tuple[1] = job destination
        #Tuple[3] = job length
        """
        joblist_len = len(joblist)
        job_dict={}
        for index in range(joblist_len):
            job_dict[index] = (joblist[index][0], #job definition
                               joblist[index][1])#, #job destination
                               #len(joblist[index][0])) #job length
        return job_dict

    def _make_buckets(self, job_dict):
        """
        Turn a job info dictionary into a dictionary bucket such that:
        key = type('Shipping' etc)    #(type('Shipping' etc),job length(int))
        value = [specific jobs]
        """
        buckets = {}
        for job_key in job_dict:
            bucket_key = job_dict[job_key][1]#,job_dict[job_key][2])
            try:
                buckets[bucket_key].append(job_dict[job_key][0])
            except:
                buckets[bucket_key] = [job_dict[job_key][0]]

        #add empty list for any missing buckets
        locations = ['Receiving', 'Shipping', 'Lab']
        mylabels = [loc for loc in locations]
        for label in mylabels:
            try:
                buckets[label]
            except:
                buckets[label] = []



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
        tuple_list = [self._generate_random_job() for i in range(self.jobs_n)]
        return tuple_list
