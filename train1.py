import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Dropout, LSTM
from tensorflow.keras.layers import Flatten, Activation, Reshape
from tensorflow.keras.layers import Conv1D, MaxPooling1D, UpSampling1D
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import BatchNormalization

from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import TensorBoard
import numpy as np

tf.logging.set_verbosity(tf.logging.ERROR)

uav_data = np.load("trainingSets.npy")

uav_label = np.load("groundTruths.npy")


uav_label = (uav_label - np.min(uav_label)) / np.max(uav_label) - np.min(uav_label)
print(uav_label.shape)
print(np.min(uav_label))
print(np.max(uav_label))
print(np.mean(uav_label))
print(np.median(uav_label))



'''
# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)


x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print('input_shape: ', input_shape)

cnn_model = Sequential()
# (28, 1)
cnn_model.add(Conv1D(32, kernel_size=3,
                 activation='relu',
                 input_shape=(28, 1)))
cnn_model.add(MaxPooling1D(pool_size=2))
cnn_model.add(Conv1D(64,  kernel_size=3, activation='relu'))
cnn_model.add(MaxPooling1D(pool_size=2))
cnn_model.add(Dropout(0.25))

cnn_model.add(Flatten())
cnn_model.add(Dense(512))
cnn_model.add(LeakyReLU(alpha=.001))
cnn_model.add(Dropout(0.25))

# print(cnn_model.summary())

timesteps = 4

lstm_model = Sequential()
lstm_model.add(Reshape((28, 512), input_shape=(28, 512)))
lstm_model.add(LSTM(1024, input_shape=(timesteps, 512), dropout=0.15, return_sequences=True))
lstm_model.add(BatchNormalization())
lstm_model.add(LSTM(512, dropout=0.15, return_sequences=True))
lstm_model.add(Dense(256))

# lstm_model.summary()


upsample_model = Sequential()
upsample_model.add(Reshape((28, 32, 8), input_shape=(28, 256)))
upsample_model.add(Conv2D(4, kernel_size=(1, 3), activation='relu'))
upsample_model.add(Conv2D(1, kernel_size=(1, 3), activation='sigmoid'))

# upsample_model.summary()

cnn_input = Input(shape=(28, 28, 1))
lstm_input = TimeDistributed(cnn_model)(cnn_input)
lstm_output = lstm_model(lstm_input)
final_output = upsample_model(lstm_output)

cnn_lstm_model = Model(inputs = cnn_input, outputs = final_output)

cnn_lstm_model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

cnn_lstm_model.fit(x_train, x_train,
                    epochs=5, batch_size=32,
                    shuffle=True,
                    validation_data=(x_test, x_test))
'''

