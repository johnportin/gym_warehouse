import gym
import envs
import numpy as np
import Q_table_module
import matplotlib.pyplot as plt




MAX_EPISODES = 1000
#MAX_TRY = 10
TASKS_N = 3
JOBS_N = 100
CAPACITY = 3
LOCATIONS_N = 3
FORKLIFTS_N = 20
FINAL_TIME = 1000
X_DIM = 5
Y_DIM = 5
REWARD_BAD_SCHEDULE = -10
NORM_CAP = 2


#hyperparameters
epsilon = 0.7  #for epsilon greedy
granularity =  1 #default = 1 is three levels

def plot(outputs):
    X = range(MAX_EPISODES)
    #X = plt.xlim(0, MAX_EPISODES)
    Y = outputs
    #plt.plot(X,Y)
    plt.scatter(X,Y)
    plt.show()

def runningAverage(mylist):
    cumulative_total = 0
    for i in range(len(mylist)):
        cumulative_total += mylist[i]
        mylist[i] = float(cumulative_total) / (i+1)
    return mylist


def epsilonGreedy(eps, state, Q):
    #action = env.action_space.sample()
    if np.random.uniform(0,1) < eps:
        action = env.action_space.sample()
    else:
        state = tuple(state) #else unhashable numpy.ndarray
        #print('Q table type = {}, length ='.format(type(Q)))
        action = np.argmax(Q.TABLE[state])
        #action = max(Q[state], key = Q[state].get)
    return action


def runEpisode():
    #initialize environment
    observation = env.reset()
    total_reward = 0
    #Q = Q_table_module.Q_table(TASKS_N, CAPACITY, NORM_CAP, env.action_space)

    for time_step in range(FINAL_TIME): #while env.done == False
        #print('Time = {} '.format(time_step) + '-'*20)
        if env.done == True:
            running_reward.append(total_reward)
            #print('Exiting at the top')
            break
        else:
            env.sim.update(time_step)
            #add loop to assign all queued forklifts or until action == wait
            for name in env.sim.forklift_names:         #loop over forklifts
                forklift = env.sim.__getattribute__(name)

                if forklift.status == '' or forklift.status == 'complete':  #take action if available forklift
                    #print('assigning forklift')
                    action = epsilonGreedy(epsilon, observation, Q)
                    #action = env.action_space.sample()
                    observation_temp = observation
                    observation, reward, done = env.step(action, time_step, forklift)
                    Q.Update_Q(observation_temp, observation, action, reward)
                    #print(observation)
        total_reward += reward
        if done == True:
            running_time.append(time_step)
            running_reward.append(total_reward)
            break


# reward = a


if __name__ == "__main__":



    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')

    running_reward = []
    running_time = []

    #initialize Q table outisde of episodes
    Q = Q_table_module.Q_table(TASKS_N, CAPACITY, NORM_CAP, env.action_space)

    for episode in range(MAX_EPISODES):
        runEpisode()
        env.render()
        env.reset()

    print(running_reward)
    #plot(runningAverage(running_reward))
    plot(runningAverage(running_time))


    #env.step()
    env.render()
    env.reset()
