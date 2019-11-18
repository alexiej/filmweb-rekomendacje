model = Sequential()
model.add(Dense(512, input_dim=self.num_observation_space, activation=relu))
model.add(Dense(256, activation=relu))
model.add(Dense(self.num_action_space, activation=linear))