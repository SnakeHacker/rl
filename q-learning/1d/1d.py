import numpy as np
import pandas as pd
import time

np.random.seed(2)

N_STATES = 6
ACTIONS = ['left', 'right']
EPSILON = 0.9
ALPHA = 0.1
LAMBDA = 0.9
MAX_EPISODES = 13
FRESH_TIME = 0.1


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions,
    )
    return table


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or (state_actions.all() == 0):
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.argmax()
    return action_name


def get_env_feedback(S, A):
    if A == 'right':
        if S == N_STATES - 2:
            S = 'terminal'
            R = 1
        else:
            S = S+1
            R = 0
    else:
        R = 0
        if S == 0:
            S = S
        else:
            S = S - 1
    return S, R


def update_env(S, episode, step_counter):
    env_list = ['-']*(N_STATES-1)+['T']
    if S == 'terminal':
        interaction = 'Episode %s: total_step = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                               ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        # print('\r{}'.format(interaction), end='')
        print(interaction)
        time.sleep(FRESH_TIME)


def rl():
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_termined = False
        update_env(S, episode, step_counter)
        while not is_termined:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + LAMBDA*q_table.iloc[S_, :].max()
            else:
                q_target = R
                is_termined = True
            q_table.loc[S, A] += ALPHA*(q_target - q_predict)
            S = S_

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table


q_table = rl()
print(q_table)
