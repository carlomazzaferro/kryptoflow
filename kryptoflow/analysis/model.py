from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
from time import time

time_steps = 10
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


class KerasModel(object):

    def __init__(self, dataset):
        self.input_shape = dataset.
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(4, input_shape=self.input_shape))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def fit(self, X, y, x_val, y_val):
        self.model.fit(X, y, epochs=15,
                       batch_size=20, verbose=2, validation_data=(x_val, y_val),
                       callbacks=[tensorboard])