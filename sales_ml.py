import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, GRU, LSTM, SimpleRNN, Dense, Concatenate
from keras import backend as K

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))

class HybridRNN:
    def __init__(self, cell_type='simple', state_sizes=[128, 64], seq_input_shape=(7, 1), current_price_shape=(1,)):
        self.cell_type = cell_type
        self.state_sizes = state_sizes
        self.seq_input_shape = seq_input_shape
        self.current_price_shape = current_price_shape
        self.model = None

    def get_layer(self, cell_type='gru', state_size=128, return_sequences=False):
        if cell_type == 'gru':
            return GRU(state_size, return_sequences=return_sequences)
        elif cell_type == 'lstm':
            return LSTM(state_size, return_sequences=return_sequences)
        else:  # simple_rnn
            return SimpleRNN(state_size, return_sequences=return_sequences)

    def build(self):
        seq_input = Input(shape=self.seq_input_shape, name='seq_input')
        current_price_input = Input(shape=self.current_price_shape, name='current_price_input')

        # RNN layers
        x = seq_input
        for i, state_size in enumerate(self.state_sizes):
            return_sequences = i < (len(self.state_sizes) - 1)
            x = self.get_layer(cell_type=self.cell_type, state_size=state_size, return_sequences=return_sequences)(x)

        # Concatenate RNN output with current price
        x = Concatenate()([x, current_price_input])

        # Output layer for regression
        output = Dense(1)(x)

        self.model = Model(inputs=[seq_input, current_price_input], outputs=output)
        self.model.compile(optimizer='rmsprop', loss=rmse, metrics=['mean_squared_error'])

    def train(self, X_train_seq, X_train_price, y_train, X_test_seq, X_test_price, y_test, epochs=20, batch_size=64):
        return self.model.fit([X_train_seq, X_train_price], y_train, epochs=epochs, batch_size=batch_size,
                              validation_data=([X_test_seq, X_test_price], y_test), verbose=1)

    def evaluate(self, X_test_seq, X_test_price, y_test):
        return self.model.evaluate([X_test_seq, X_test_price], y_test, verbose=0)



csv_files = ['FOODS_1.csv', 'FOODS_2.csv', 'FOODS_3.csv', 'HOBBIES_1.csv', 'HOBBIES_2.csv', 'HOUSEHOLD_1.csv', 'HOUSEHOLD_2.csv']

for file_name in csv_files:
    try:
        # Load the dataset
        df = pd.read_csv(file_name)

        # Prepare the data
        y = df['sales_change']
        X = df.drop(columns=['sales_change'])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        X_train_seq = X_train[:, :7].reshape(-1, 7, 1)
        X_train_price = X_train[:, -1].reshape(-1, 1)
        X_test_seq = X_test[:, :7].reshape(-1, 7, 1)
        X_test_price = X_test[:, -1].reshape(-1, 1)

        # Create and train the model
        hybrid_rnn = HybridRNN(cell_type='gru', state_sizes=[128, 256], seq_input_shape=(7, 1), current_price_shape=(1,))
        hybrid_rnn.build()
        history = hybrid_rnn.train(X_train_seq, X_train_price, y_train, X_test_seq, X_test_price, y_test, epochs=20, batch_size=64)

        # Extract and print the RMSE from the last epoch of validation
        loss = history.history['val_loss'][-1]
        print(f"Model trained on {file_name}: RMSE={loss:.4f}")

        # Save the model
        model_path = file_name.replace('.csv', '_rnn_model.h5')
        hybrid_rnn.model.save(model_path)
        print(f"Model saved as {model_path}")

    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")





