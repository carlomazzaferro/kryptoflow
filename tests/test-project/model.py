from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam

from time import time


time_steps = 8
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


class KerasModel(object):

    def __init__(self, dims=None, store=True):
        self.input_shape = dims
        self.store = store
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(32, input_shape=self.input_shape, return_sequences=False))
        adam = Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer=adam)
        return model

    def fit(self, X, y, x_val, y_val, epochs=15):

        self.model.fit(X, y, epochs=epochs,
                       batch_size=64, verbose=2, validation_data=(x_val, y_val),
                       callbacks=[tensorboard])
