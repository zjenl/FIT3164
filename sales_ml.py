import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))

class BaseRNN:
    def __init__(self, cell_type='simple', state_sizes=[128, 64], input_shape=(1, 8)):
        self.cell_type = cell_type
        self.state_sizes = state_sizes
        self.input_shape = input_shape
        self.model = None

    @staticmethod
    def get_layer(cell_type='gru', state_size=128, return_sequences=False):
        if cell_type == 'gru':
            return tf.keras.layers.GRU(state_size, return_sequences=return_sequences)
        elif cell_type == 'lstm':
            return tf.keras.layers.LSTM(state_size, return_sequences=return_sequences)
        else:  # simple_rnn
            return tf.keras.layers.SimpleRNN(state_size, return_sequences=return_sequences)

    def build(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=self.input_shape))

        for i, state_size in enumerate(self.state_sizes):
            return_sequences = i < (len(self.state_sizes) - 1)
            layer = self.get_layer(cell_type=self.cell_type, state_size=state_size, return_sequences=return_sequences)
            model.add(layer)

        # Output layer for regression
        model.add(tf.keras.layers.Dense(1))

        self.model = model

    def compile_and_train(self, X_train, y_train, X_test, y_test, opt, epochs=20, batch_size=64):
        self.model.compile(optimizer=opt, loss=rmse, metrics=['mean_squared_error'])
        history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                                 validation_data=(X_test, y_test), verbose=1)
        return history

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test, verbose=0)


# Load the dataset
df = pd.read_csv('FOODS_1.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Reshape input to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

cell_types = ['simple_rnn', 'gru', 'lstm']
state_sizes_list = [[64, 128], [128, 256]]

results = {}

for state_sizes in state_sizes_list:
    for cell_type in cell_types:
        print(f"Training with {cell_type.upper()} and state sizes {state_sizes}")
        rnn = BaseRNN(cell_type=cell_type, state_sizes=state_sizes, input_shape=(X_train.shape[1], X_train.shape[2]))
        rnn.build()
        opt = tf.keras.optimizers.RMSprop(learning_rate=0.001)
        history = rnn.compile_and_train(X_train, y_train, X_test, y_test, opt=opt, epochs=20, batch_size=64)

        mse = history.history['val_loss'][-1]  # Use validation loss as a proxy for MSE

        # Store the results
        results.setdefault(str(state_sizes), {})[cell_type] = mse

# Print the summarized results
for state_sizes, cell_results in results.items():
    print(f"\nState Sizes: {state_sizes}")
    for cell_type, rmse in cell_results.items():
        print(f"{cell_type}: RMSE={rmse:.4f}")



