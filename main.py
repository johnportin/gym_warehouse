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

def epsilon_greedy(eps):
    if np.random.uniform(0,1) < eps:
        action = env.action_space.sample()
    else:
        action = np.argmax(q_table[state])


def simulate():
    for episode in range(MAX_EPISODES):

        #initialize environment
        state = env.reset()
        total_reward = 0

        #do at most 10 queue updates
#        for time_step in range(MAX_TRY):






if __name__ == "__main__":



    #initial testing of environment to make sure it initalizes.
    env = gym.make('Warehouse-v0')
    #initialize q table with zeros as dictionary
    q_table = {i : np.zeros(TASKS_N * LOCATIONS_N + LOCATIONS_N + FORKLIFTS_N + 1) for i in range(env.action_space.n)}

    env.step()
    env.render()
    env.reset()
