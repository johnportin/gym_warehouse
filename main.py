import gym
import envs
import numpy as np



MAX_EPISODES = 10
MAX_TRY = 10
TASKS_N = 1
CAPACITY = 2
LOCATIONS_N = 1
LOC1 = 0
FORKLIFTS_N = 3
FINAL_TIME = 1000

REWARD_BAD_SCHEDULE = -10

#hyperparameters
epsilon = 0.7  #for epsilon greedy
granularity =  1 #default = 1 is three levels

def epsilonGreedy(eps):
    if np.random.uniform(0,1) < eps:
        action = env.action_space.sample()
    else:
        action = np.argmax(q_table[state])

def initQ():
    #calculat total number of states:
    total_states = TASKS_N * LOCATIONS_N + LOCATIONS_N + FORKLIFTS_N + 1

    #initialize a (size of actions space) x (total states) array of zeros
    Q = np.zeros((env.action_space.n, total_states))
    return Q



def simulateOnce():
    #initialize environment
    Q = initQ()
    observation = env.reset()
    total_reward = 0

    for time_step in range(FINAL_TIME): #while env.done == False
        if env.done == True:
            break
        else:
            #add loop to assign all queued forklifts or until action == wait
            for name in env.sim.forklift_names:         #loop over forklifts
                forklift = env.sim.__getattribute__(name)

                if forklift.status == '' or forklift.status == 'complete':  #take action if available forklift
                    action = epsilonGreedy(epsilon)
                    try:    #assign job and update environment if possible
                        forklift.task_list = env.buckets[action][0]
                        forklift.update_travel_time(time_step)
                        observation, reward, done, _ = env.step(action)
                    except: #otherwise, take a negative reward
                        reward -= REWARD_BAD_SCHEDULE #Definitely need to tune this value
            #tally up the reward and update the Q table
        #report total results



if __name__ == "__main__":



    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')
    #initialize q table with zeros as dictionary

    env.step(action = 0)
    env.render()
    env.reset()
