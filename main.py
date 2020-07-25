import gym
import envs
import numpy as np



MAX_EPISODES = 10
MAX_TRY = 10
TASKS_N = 3
JOBS_N = 30
CAPACITY = 3
LOCATIONS_N = 3
FORKLIFTS_N = 20
FINAL_TIME = 10000
X_DIM = 5
Y_DIM = 5
REWARD_BAD_SCHEDULE = -10


#hyperparameters
epsilon = 0.7  #for epsilon greedy
granularity =  1 #default = 1 is three levels

def epsilonGreedy(eps):
    action = env.action_space.sample()
    '''
    if np.random.uniform(0,1) < eps:
        action = env.action_space.sample()
    else:
        action = np.argmax(q_table[state])
    '''

def initQ():
    #calculat total number of states:
    total_states = TASKS_N * LOCATIONS_N + LOCATIONS_N + FORKLIFTS_N + 1

    #initialize a (size of actions space) x (total states) array of zeros
    Q = np.zeros((TASKS_N * LOCATIONS_N + 1, total_states))
    return Q



def runEpisode():
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
                    observation, reward, done = env.step(action, time_step, forklift)
        print(observation)
        print(time_step)
        total_reward += reward
        if done == True:
            env.render()
            env.reset()
            break





if __name__ == "__main__":



    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')
    #initialize q table with zeros as dictionary
    runEpisode()

    #env.step()
    env.render()
    env.reset()
