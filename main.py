import gym
import envs
import numpy as np
import Q_table_module




MAX_EPISODES = 10
MAX_TRY = 10
TASKS_N = 3
JOBS_N = 10
CAPACITY = 3
LOCATIONS_N = 3
FORKLIFTS_N = 3
FINAL_TIME = 1000
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


def runEpisode():
    #initialize environment
    observation = env.reset()
    total_reward = 0
    Q = Q_table_module.Q_table(TASKS_N, CAPACITY, env.action_space)

    for time_step in range(FINAL_TIME): #while env.done == False
        print('Time = {} '.format(time_step) + '-'*20)
        if env.done == True:
            print('Exiting at the top')
            break
        else:
            env.sim.update(time_step)
            #add loop to assign all queued forklifts or until action == wait
            for name in env.sim.forklift_names:         #loop over forklifts
                forklift = env.sim.__getattribute__(name)

                if forklift.status == '' or forklift.status == 'complete':  #take action if available forklift
                    print('assigning forklift')
                    #action = epsilonGreedy(epsilon)
                    action = env.action_space.sample()
                    observation_temp = observation
                    observation, reward, done = env.step(action, time_step, forklift)
                    Q.Update_Q(observation_temp, observation, action, reward)
                    #print(observation)
        total_reward += reward
        if done == True:
            print('Exiting at the bottom')
            env.render()
            env.reset()
            break





if __name__ == "__main__":



    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')
    print('buckets = {}'.format(env.sim.buckets))
    #initialize q table with zeros as dictionary
    runEpisode()

    #env.step()
    env.render()
    env.reset()
