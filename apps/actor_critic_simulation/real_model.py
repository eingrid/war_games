from keras import backend as K
from keras.layers import Dense, Activation, Input
from keras.models import Model, load_model
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras import regularizers
import tensorflow as tf
import numpy as np
import sys
from keras.utils import custom_object_scope
from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()

class Agent(object):
    def __init__(self, alpha, beta, gamma=0.5, n_actions=5,
                layer1_size=4096, layer2_size=2048, layer3_size = 512, layer4_size = 512, input_dims=25,n_ally_units=1):

        self.epsilon = 0.5
        
        total_possible_actions = n_actions**n_ally_units
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.input_dims = input_dims
        self.fc1_dims = layer1_size
        self.fc2_dims = layer2_size
        self.fc3_dims = layer3_size
        self.fc4_dims = layer4_size
        self.n_actions = total_possible_actions

        with tf.device("/GPU:0"):
            self.actor, self.critic, self.policy = self.build_actor_critic_network()
        self.action_space = [i for i in range(total_possible_actions)]

    def build_actor_critic_network(self):
        inputs = Input(shape=(self.input_dims,))
        delta = Input(shape=[1])
        dense1 = Dense(self.fc1_dims, activation='relu',)(inputs)
        dense2 = Dense(self.fc2_dims, activation='relu',)(dense1)
        dense3 = Dense(self.fc3_dims, activation='relu',)(dense2)
        # dense4 = Dense(self.fc4_dims, activation='relu',)(dense3)
        probs = Dense(self.n_actions, activation='softmax')(dense3)
        values = Dense(1, activation='linear')(dense3)

        def custom_loss(y_true, y_pred):
            print('calc loss')
            out = K.clip(y_pred, 1e-8, 1-1e-8)
            log_lik = y_true*K.log(out)
            loss = K.sum(-log_lik*delta)
            print('calc loss finish')

            return loss

        actor = Model(inputs=[inputs, delta], outputs=[probs])

        actor.compile(optimizer=Adam(lr=self.alpha), loss=custom_loss)

        critic = Model(inputs=[inputs], outputs=[values])

        critic.compile(optimizer=Adam(lr=self.beta), loss='mean_squared_error')

        policy = Model(inputs=[inputs], outputs=[probs])

        return actor, critic, policy

    def choose_action(self, observation):
        state = observation[np.newaxis, :]
        probabilities = self.policy.predict(state)[0]
        # print("PROBS FOR ACTIONS ", probabilities)
        # TODO set some probs to zero if action is not possible
        # print(probabilities)
        
        action = self.select_action(probabilities)#np.random.choice(self.action_space, p=probabilities)
        # print("TOTAL ACTIONS", len(self.action_space)," choosen action ", action)

        return action




# Action selection with epsilon-greedy strategy
    def select_action(self,probabilities):
            # Define epsilon value (controls exploration)
        if np.random.rand() < self.epsilon:
            # Random action for exploration
            # print('###### random action')
            return np.random.choice(self.action_space)
        else:
            # Choose action with highest probability for exploitation
            return np.random.choice(self.action_space, p=probabilities)
        
    def learn(self, state, action, reward, state_, done):
        state = state[np.newaxis,:]
        state_ = state_[np.newaxis,:]
        critic_value_ = self.critic.predict(state_)
        critic_value = self.critic.predict(state)

        target = reward + self.gamma*critic_value_*(1-int(done))
        delta =  target - critic_value

        actions = np.zeros([1, self.n_actions])
        actions[np.arange(1), action] = 1

        self.actor.fit([state, delta], actions, verbose=0)

        self.critic.fit(state, target, verbose=0)

    def save_models(self, actor_filename='actor.h5', critic_filename='critic.h5'):
            self.actor.save(actor_filename)
            self.critic.save(critic_filename)
    def custom_loss(self, y_true, y_pred):
        # Define your custom loss function here
        print('calc loss')
        out = K.clip(y_pred, 1e-8, 1-1e-8)
        log_lik = y_true * K.log(out)
        loss = K.sum(-log_lik)
        print('calc loss finish')
        return loss
    
    def load_models(self, actor_filename='actor.h5', critic_filename='critic.h5'):
        # Load actor and critic models for inference
        with custom_object_scope({'custom_loss': self.custom_loss}):
            self.actor = load_model(actor_filename)
            self.critic = load_model(critic_filename)


# # Example usage:
# num_units = 3
# num_actions = 5
# predicted_action_number = 120  # Replace this with the predicted action number
# result = map_action_number_to_vector(predicted_action_number, num_units, num_actions)