"""
Everything related to the Q table is included in this class
"""
import numpy as np
import pandas as pd
import pickle
import time

class Q_table:
    def __init__(self,
                 max_task_len = 4,
                 max_capacity = 3,
                 norm_cap = 3,
                 action_space = None,
                 learning_rate = 0.1,
                 discount = 0.997):
        self.LOC_CAPACITY = max_capacity; # Number of forklifts we can overlay at the 3 processing places
        self.MAX_TASK_LEN = max_task_len; # Task length starts from 2 to MAX_TASK_LEN, including boundaries
        self.LOCATIONS_N = 3; # 3 Processing places
        self.CAP_SHIP = max_capacity # max capacity at shipping
        self.CAP_LAB = max_capacity
        self.CAP_RECEIVE = max_capacity
        self.NORM_CAP = norm_cap # normalized cap for each kind of job type
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount = discount
        self.OBS_DICT=self._make_observation_dict()
        ##### This is the actual Q table #####
        self.TABLE = self._init_Q()
        self.TABLE_df = self._conv_to_dataframe()
        ######################################
    
    def Export_Q(self):
        with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
            pickle.dump(self.TABLE, f)
    
    def Import_Q(self, Q_table_filename):
        with open(Q_table_filename, "rb") as f:
            self.TABLE = pickle.load(f)

    def Update_Q(self, current_obs, new_obs, action, reward):
        """
        Update the Q table.
        """
        new_obs = tuple(new_obs) ##added: because nparray is unhashable
        current_obs = tuple(current_obs)
        #print(new_obs)
        max_future_q = np.max(list(self.TABLE[new_obs].values()))
        current_q = self.TABLE[current_obs][action]

        new_q = (1 - self.learning_rate) * current_q + \
            self.learning_rate * (reward + self.discount * max_future_q)
        self.TABLE[current_obs][action] = new_q
            
    def Update_Q_df(self, current_obs, new_obs, action, reward):
        """
        Update the Q table. Slightly different being in dataframe form
        """
        new_obs = tuple(new_obs) ##added: because nparray is unhashable
        current_obs = tuple(current_obs)
        max_future_q = max(self.TABLE_df.loc[new_obs])
        current_q = self.TABLE_df.loc[current_obs, action]

        new_q = (1 - self.learning_rate) * current_q + \
            self.learning_rate * (reward + self.discount * max_future_q)
        self.TABLE_df.loc[current_obs, action] = new_q
        
    def _conv_to_dataframe(self):
        """
        Convert to a dataframe table
        """
        df = pd.DataFrame.from_dict(self.TABLE, orient='index')
        return df
        

    def _init_Q(self):
        """
        Q table initialization: Q[actual observation][actual action]
        action_space needs to be a list of tuples
        """
        Q = {}
        for observation in self.OBS_DICT.values(): #initialize the q-table as 0 for each action, state pair
            Q[observation] = {action: 0 for action in range(self.action_space.n)}#env.action_space.n)]
        return Q

    def _make_observation_dict(self):
        OBS_DICT = {}
        """
        Observations have the following structure:
        (Num of job Type Shipping remained,
        Num of job Type Lab remained,
        Num of job Type Receiving remained,
        Capacity at Shipping currently,
        Capacity at Lab currently,
        Capacity at Receiving currently,
        Whether there's an available forklift) in ***tuple*** form
        This function associates all possible observation state
        """
        key = 0
        job_load = list(range(self.NORM_CAP + 1)) # all allowed job load (normalized) for each type: 0,1,2,3
        destinations = ['Shipping', 'Lab', 'Receiving']
        if_forklift_available = [True, False]
        for loadS in job_load:
            for loadL in job_load:
                for loadR in job_load:
                    for cap_ship in range(self.CAP_SHIP+1):
                        for cap_lab in range(self.CAP_LAB+1):
                            for cap_receive in range(self.CAP_RECEIVE+1):
                                for if_avai_fl in if_forklift_available:
                                    OBS_DICT[key] = (loadS,loadL,loadR,
                                                     cap_ship,cap_lab,cap_receive,
                                                     if_avai_fl)
                                    key += 1


        return OBS_DICT
