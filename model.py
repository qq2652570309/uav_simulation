import os
os.environ["CUDA_VISIBLE_DEVICES"]="2"
import tensorflow as tf
from tensorflow.python.ops import math_ops
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout, LSTM, Conv2DTranspose, Conv3DTranspose
from tensorflow.keras.layers import Flatten, Activation, Reshape
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow.keras import backend as K
import numpy as np

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Cnn_Lstm_Model:
    def __init__(self):
        self.model = None

        uav_data = np.load("trainingSets1.npy")
        print('raw uav_data: ', uav_data.shape) # (1000, 30, 16, 16, 4)

        uav_label = np.load("groundTruths.npy")
        print('raw uav_label: ', uav_label.shape) # (1000, 30, 16, 16)

        # uav_label = (uav_label - np.min(uav_label)) / np.max(uav_label) - np.min(uav_label)
        # print('uav_label min: ', np.min(uav_label))
        # print('uav_label max: ', np.max(uav_label))
        # print('uav_label mean: ', np.mean(uav_label))
        # print('uav_label median: ', np.median(uav_label))

        data_size = int(len(uav_data) * 0.85)

        # (x_train, y_train) = uav_data[:850], uav_label[:850]
        # (x_test, y_test) = uav_data[850:], uav_label[850:]
        (x_train, y_train) = uav_data[:data_size], uav_label[:data_size]
        (x_test, y_test) = uav_data[data_size:], uav_label[data_size:]



        cnn_model = Sequential()
        cnn_model.add(Conv2D(8, kernel_size=(2, 2),
                        activation='relu',
                        input_shape=(16, 16, 4)))
        cnn_model.add(Conv2D(16, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(MaxPooling2D(pool_size=(2,2)))
        # cnn_model.add(Conv2D(4, kernel_size=(2, 2), activation='relu'))
        # cnn_model.add(MaxPooling2D(pool_size=(2,2)))
        cnn_model.add(Flatten())
        cnn_model.summary()


        lstm_model = Sequential()
        lstm_model.add(LSTM(4096, input_shape=(30, 1024), dropout=0.15, return_sequences=False))
        lstm_model.add(BatchNormalization())
        lstm_model.add(Dense(2048))
        lstm_model.add(BatchNormalization())
        lstm_model.add(LeakyReLU(alpha=.001))
        lstm_model.add(Dense(1024))
        lstm_model.add(BatchNormalization())
        lstm_model.add(LeakyReLU(alpha=.001))
        lstm_model.summary()



        upsample_model = Sequential()
        upsample_model.add(Reshape((16, 8, 8, 1), input_shape=(1, 1024)))
        upsample_model.add(Conv3DTranspose(2, kernel_size=(4, 3, 3), activation='relu'))
        upsample_model.add(BatchNormalization())
        upsample_model.add(Conv3DTranspose(4, kernel_size=(5, 3, 3), activation='relu'))
        upsample_model.add(BatchNormalization())
        upsample_model.add(Conv3DTranspose(2, kernel_size=(4, 3, 3), activation='relu'))
        upsample_model.add(BatchNormalization())
        upsample_model.add(Conv3DTranspose(1, kernel_size=(5, 3, 3), activation='relu'))
        upsample_model.add(BatchNormalization())
        upsample_model.add(Reshape((30, 16, 16)))
        upsample_model.summary()


        # cnn_input = (?, 30, 16, 16, 4)

        cnn_input = Input(shape=uav_data[0].shape)
        print('input shape: ',cnn_input.shape) # (?, 30, 16, 16, 4)
        lstm_input = TimeDistributed(cnn_model)(cnn_input)
        lstm_output = lstm_model(lstm_input)
        final_output = upsample_model(lstm_output)

        cnn_lstm_model = Model(inputs=cnn_input, outputs=final_output)

        def weighted_binary_crossentropy(weights):
            def w_binary_crossentropy(y_true, y_pred):
                return tf.keras.backend.mean(tf.nn.weighted_cross_entropy_with_logits(
                    y_true,
                    y_pred,
                    weights,
                    name=None
                ), axis=-1)
            return w_binary_crossentropy

        weighted_loss = weighted_binary_crossentropy(weights=2)


        def recall(y_true, y_pred):
            y_true = math_ops.cast(y_true, 'float32')
            y_pred = math_ops.cast(y_pred, 'float32')
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        cnn_lstm_model.compile(optimizer='adadelta', loss=weighted_loss, metrics=[recall])

        self.model = cnn_lstm_model

    def train(self):
        