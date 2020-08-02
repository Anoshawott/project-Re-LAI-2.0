from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import tensorflow as tf

from player_interaction import PlayerAI
from env_reset import EnvReset
# from choice_create import ChoiceCreate

from collections import deque

from tqdm import tqdm

import time
import numpy as np
import random
import os
import subprocess
import pickle
import copy
import subprocess
from DirectKeys import PressKey, ReleaseKey, BACK

FROM = 0

REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1000
MINIBATCH_SIZE = 6
DISCOUNT = 0.99
UPDATE_TARGET_EVERY = 5
MIN_REWARD = -200

EPISODES = 20_000

# Consider changing epsilon??
epsilon = 1
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

# Adjust below condition to true episode number
thing = 0
while thing < FROM + 1:
    epsilon *= EPSILON_DECAY
    epsilon = max(MIN_EPSILON, epsilon)
    thing+=1

AGGREGATE_STATS_EVERY = 50
SHOW_PREVIEW = False

MODEL_NAME = '2X12'

class AIEnv:
    RETURN_DATA = True
    ACTION_SPACE_SIZE = 12
    OBSERVATION_SPACE_VALUES = (361,640,3)
    # Reward and Penalty Values
    # also need a reward for mana and hp increases, but make this minimal compared to others 
    rewards = {'enemy_damage': 1, 'player_damage':1, 'death':1000, 'kill':1000}

    def reset(self):
        # further this function so that the whole game resets with a new game each time an episode has past
        # use the following code to close windows from within this function: subprocess.call("taskkill /f /im notepad.exe", shell=True)
        # have timed intervals between each step in the reset process... --> just need to automate setting up a new game
        # need to also determine how to save each model between episodes...
        # EnvReset().game_reset()
        PressKey(BACK)
        time.sleep(0.1)
        ReleaseKey(BACK)

        for i in list(range(10))[::-1]:
            print(i+1)
            time.sleep(1)

        PressKey(BACK)
        time.sleep(0.1)
        ReleaseKey(BACK)
        
        #Start!
        self.play_ai = PlayerAI()

        self.episode_step = 0

        if self.RETURN_DATA:
            observation = self.play_ai.new_data()
        # else?
        return observation
    
    def step(self, action, last_obs=None, count=None): 
        self.episode_step+=1

        self.play_ai.action(action)
        
        done = False

        if self.RETURN_DATA:
            new_observation = self.play_ai.new_data()
        
        net_reward = 0
        ### Reward and Penalty Conditions
        # try:
        #     if int(new_observation['output_data']['d']) == 1: #int(new_observation['output_data']['hp']) == 0
        #         done = True
        #         # new = int(new_observation['output_data']['d'])    
        #         # old = int(last_obs['output_data']['d'])
        #         delta = 1
        #         total_penalty = -self.rewards['d'] * delta
        #         net_reward += total_penalty
        #         print('DEAD!')
        # except:
        #     None
        try:
            if last_obs['output_data']['player_damange'] == '' and int(new_observation['output_data']['player_damange']) == 0:
                net_reward += -self.reward['death']
                done = True
                print('DEAD!')
        except:
            None

        tmp_new = copy.deepcopy(new_observation)
        tmp_old = copy.deepcopy(last_obs)

        # Have a list that appends turrets that have been destroyed to have them removed and then added to the distance left to turret
        # use min-max method to optimising distance reward reward since the ai rn is prioritising reaching the nexus before destroying
        # anything else first...
        output_data_comp = new_observation['output_data'].items() & last_obs['output_data'].items()

        if len(output_data_comp) != 2:
            for i in output_data_comp:
                del tmp_new['output_data'][i[0]]
                del tmp_old['output_data'][i[0]]
            for k in tmp_new['output_data']:
                if k == 'enemy_damage':
                    try:
                        new = int(new_observation['output_data'][k])
                        old = int(last_obs['output_data'][k])
                        delta = new - old
                        print(k)
                        if int(last_obs['output_data'][k]) > 0 and int(new_observation['output_data'][k]) == 0:
                                net_reward += self.reward['kill']
                                print('SMASHED!')
                        if delta > 0:
                            total_reward = self.rewards[k] * delta
                            net_reward += total_reward
                            print(new)
                            print(old)
                            print('2')
                        # if k == 'hp' and new == 0:
                        #     done = True    
                        #     total_penalty = self.rewards[k] * delta
                        #     net_reward += total_penalty
                        #     print('DEAD!')
                    except:
                        None
                    
                else:
                    try:
                        new = int(new_observation['output_data'][k])    
                        old = int(last_obs['output_data'][k])
                        delta = new - old
                        total_penalty = -self.rewards[k] * delta
                        net_reward += total_penalty
                        print('3')
                        if int(last_obs['output_data'][k]) > 0 and int(new_observation['output_data'][k]) == 0:
                            net_reward += -self.reward['death']
                            done = True
                            print('DEAD!')
                    except:
                        None                     

        return new_observation, net_reward, done, count

env = AIEnv()

ep_rewards = [-200]

random.seed(1)
np.random.seed(1)
tf.random.set_seed(1)

# if not os.path.isdir('dql_models'):
#     os.makedirs('dql_models')

class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.create_file_writer(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass
    
    # def _write_logs(self, logs, index):
    #     for name, value in logs.items():
    #         if name in ['batch', 'size']:
    #             continue
    #         summary = tf.summary()
    #         summary_value = summary.value.add()
    #         summary_value.simple_value = value
    #         summary_value.tag = name
    #         self.writer.add_summary(summary, index)
    #     self.writer.flush()

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

class DQNAgent:
    def __init__(self):

        # main model --> gets trained every step
        self.model = self.create_model()

        # Loading from given run
        # self.model = tf.keras.models.load_model('dql_models4/2X12__ep__235.00_-200.00max_-501909.33avg_-1003618.66min__1595411064.model')

        # target model --> this is what we .predict against every step
        self.target_model = self.create_model() 
        # self.target_model = tf.keras.models.load_model('dql_models4/2X12__ep__235.00_-200.00max_-501909.33avg_-1003618.66min__1595411064.model')
        self.target_model.set_weights(self.model.get_weights())

        # handles batch samples so to attain stability in training; prevent overfitting
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        self.tensorboard = ModifiedTensorBoard(log_dir='logs/{}-{}'.format(MODEL_NAME, int(time.time())))

        self.target_update_counter = 0


    def create_model(self):
        model = Sequential()
        model.add(Conv2D(12, (3,3), input_shape=env.OBSERVATION_SPACE_VALUES))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Conv2D(12, (3,3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(8))

        model.add(Dense(env.ACTION_SPACE_SIZE, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model
    
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1,*state.shape)/255)[0]

    def train(self, terminal_state, step):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return
        
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        current_states = np.array([transition[0]['img'] for transition in minibatch])/255
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array([transition[3]['img'] for transition in minibatch])/255
        future_qs_list = self.target_model.predict(new_current_states)

        X=[]
        y=[]

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state['img'])
            y.append(current_qs)
        
        self.model.fit(np.divide(np.array(X), 255), np.array(y), batch_size=MINIBATCH_SIZE,
                        verbose=0, shuffle=False)
        # , callbacks=[self.tensorboard] if terminal_state else None
        print('fitting?')

        if terminal_state:
            self.target_update_counter += 1 
        
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0        


agent = DQNAgent()

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

for episode in tqdm(range(1, EPISODES+1), ascii=True, unit='episode', initial=FROM):
    agent.tensorboard.step = episode

    episode_reward = 0
    step = 1
    current_state = env.reset()

    done = False
    
    num = 0
    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(agent.get_qs(current_state['img']))
        else:
            action = np.random.randint(0,env.ACTION_SPACE_SIZE)
        print(step)
        print(action)
        try:
            new_state, reward, done, num = env.step(action=action, last_obs=current_state, count=num)
            episode_reward += reward
            print('episode_reward:', episode_reward)
            print('-------------------')
            agent.update_replay_memory((current_state, action, reward, new_state, done))
            agent.train(done, step)

            current_state = copy.deepcopy(new_state)
            step += 1
        except:
            # time.sleep(40)
            # done = True
            # subprocess.call("taskkill /f /im \"LeagueClient.exe\"", shell=True)
            # time.sleep(5)
            None
        
    
    # NEED TO ADD FUNCTION TO SAVE EVERY EPISODE!!! --> every 5 episodes?

    print('episode_reward:', episode_reward)
    # Append episode reward to a list and log stats (every given number of episodes)
    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        # agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

        # Save model, but only when min reward is greater or equal a set value
        if average_reward >= MIN_REWARD:
            agent.model.save(f'dql_best_avg/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

    if (episode+FROM)%5 == 0:
        agent.model.save(f'dql_models1/{MODEL_NAME}__ep_{episode+FROM:_>7.2f}_{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

    print('avg_reward:', average_reward)
    print('min_reward:', min_reward)
    print('max_reward:', max_reward)

    # Decay epsilon 

    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)