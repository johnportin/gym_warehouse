import gym
import envs
import os
import numpy as np
import Q_table_module
import matplotlib.pyplot as plt




MAX_EPISODES = 2000
#MAX_TRY = 10
TASKS_N = 3
JOBS_N = 100
CAPACITY = 3
LOCATIONS_N = 3
FORKLIFTS_N = 13
FINAL_TIME = 600
X_DIM = 5
Y_DIM = 5
NORM_CAP = 2


#hyperparameters
EPSILON = 0.995  #for epsilon greedy
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


def runEpisode(epsilon):
    #initialize environment
    observation = env.reset()
    total_reward = 0
    #Q = Q_table_module.Q_table(TASKS_N, CAPACITY, NORM_CAP, env.action_space)

    for time_step in range(FINAL_TIME): #while env.done == False
        #print('Time = {} '.format(time_step) + '-'*20)
        if env.done == True:
            return time_step, total_reward
            #running_reward.append(total_reward)
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
                    if done == True:
                        break
                    #print(observation)
        total_reward += reward
        if done == True:
            return time_step, total_reward
            #running_time.append(time_step)
            #running_reward.append(total_reward)
            break
    return time_step, total_reward


# reward = a


if __name__ == "__main__":


    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')

    try:
        file = open('sample1.txt', 'a')
        file.close()
    except:
        file = open('sample1.txt', 'w+')
        file.write('episode, time, episode_reward\n')
        file.close()

    running_reward = []
    running_time = []

    #initialize Q table outisde of episodes
    Q = Q_table_module.Q_table(TASKS_N, CAPACITY, NORM_CAP, env.action_space)

    epsilon = EPSILON
    for episode in range(MAX_EPISODES):

        time, reward = runEpisode(epsilon)
        running_time.append(time)
        running_reward.append(reward)
        #env.render()
        epsilon *= EPSILON
        if episode % 10 == 0:
            data_points = [episode, time, reward]
            print('episode = {} \ttime = {} \treward = {}'.format(*data_points))
            file = open('sample1.txt', 'a')
            data_points_str = '{}, {}, {} \n'.format(episode, time, reward)
            #file.write(str(episode) + ', ' + str(time) + ', ' + str(reward) + '\n')
            file.write(data_points_str)
            file.close()

        if episode % 1000 == 0:
            epsilon = EPSILON





    #plot(runningAverage(running_reward))
    #plot(running_time)
    plot(running_reward)


    #env.step()
    env.render()
    env.reset()
