"""
Everything related to the Q table is included in this class
"""
import numpy as np

class Q_table:
    def __init__(self,
                 max_task_len = 4,
                 max_capacity = 5, 
                 action_space = None,
                 learning_rate = 0.9, 
                 discount = 0.6):
        self.LOC_CAPACITY = max_capacity; # Number of forklifts we can overlay at the 3 processing places
        self.MAX_TASK_LEN = max_task_len; # Task length starts from 2 to MAX_TASK_LEN, including boundaries
        self.LOCATIONS_N = 3; # 3 Processing places
        self.CAP_SHIP = max_capacity # max capacity at shipping
        self.CAP_LAB = max_capacity
        self.CAP_RECEIVE = max_capacity
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount = discount
        self.OBS_DICT=self._make_observation_dict()
        ##### This is the actual Q table ##### 
        self.TABLE = self.init_Q()
        ######################################        
    
    def Update_Q(self, current_obs, new_obs, action, reward):
        """
        Update the Q table
        """
        max_future_q = np.max(list(self.TABLE[new_obs].values()))
        current_q = self.TABLE[current_obs][action]
        
        new_q = (1 - self.learning_rate) * current_q + \
            self.learning_rate * (reward + self.discount * max_future_q)
        self.TABLE[current_obs][action] = new_q
        
    def init_Q(self):
        """
        Q table initialization: Q[actual observation][actual action]
        action_space needs to be a list of tuples
        """
        Q = {}
        for observation in self.OBS_DICT.values():
            Q[observation] = {action: 0 for action in self.action_space}#env.action_space.n)]
        return Q
    
    def _make_observation_dict(self):
        OBS_DICT = {}
        """
        Observations have the following structure:
        (Task Length,
        Destination Type,
        Capacity at Shipping,
        Capacity at Lab,
        Capacity at Receiving,
        Whether there's an available forklift) in ***tuple*** form
        This function associates all possible observation state
        """
        key = 0
        destinations = ['Shipping', 'Lab', 'Receiving']
        if_forklift_available = [True, False]
        for task_len in range(2, self.MAX_TASK_LEN + 1):
            for destination in destinations:
                for cap_ship in range(self.CAP_SHIP+1):
                    for cap_lab in range(self.CAP_LAB+1):
                        for cap_receive in range(self.CAP_RECEIVE+1):
                            for if_avai_fl in if_forklift_available:
                                OBS_DICT[key] = (task_len,destination,cap_ship,cap_lab,cap_receive,if_avai_fl)
                                key += 1
        return OBS_DICT
    

        
