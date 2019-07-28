import os
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
from tensorflow.keras import metrics
import numpy as np


os.environ["CUDA_VISIBLE_DEVICES"]="2"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Cnn_Lstm_Model:
    def __init__(self, trs=None, grt=None):

        uav_data = np.load(trs)
        # uav_data = uav_data[:2]
        print('uav_data: ', uav_data.shape) # (1000, 30, 16, 16, 4)

        uav_label = np.load(grt)
        # uav_label = uav_label[:2]
        print('uav_label: ', uav_label.shape) # (1000, 30, 16, 16)

        data_size = int(len(uav_data) * 0.85)

        # (x_train, y_train) = uav_data[:850], uav_label[:850]
        # (x_test, y_test) = uav_data[850:], uav_label[850:]
        (x_train, y_train) = uav_data[:data_size], uav_label[:data_size]
        (x_test, y_test) = uav_data[data_size:], uav_label[data_size:]


        cnn_model = Sequential()
        cnn_model.add(Conv2D(8, kernel_size=(3, 3),
                        activation='relu',
                        input_shape=(16, 16, 4)))
        cnn_model.add(Conv2D(16, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
        cnn_model.add(MaxPooling2D(pool_size=(2,2)))
        # cnn_model.add(Conv2D(4, kernel_size=(2, 2), activation='relu'))
        # cnn_model.add(MaxPooling2D(pool_size=(2,2)))
        cnn_model.add(Flatten())
        cnn_model.summary()

        # (30*1024) = 2^15, 16384 = 2^14, 4096 = 2^12, 2014 = 2^10 
        lstm_model = Sequential()
        lstm_model.add(LSTM(512, input_shape=(30, 512), dropout=0.0, return_sequences=True))
        lstm_model.add(TimeDistributed(Dense(256)))
        lstm_model.add(TimeDistributed(Reshape((16, 16))))
        lstm_model.summary()


        # upsample_model = Sequential()
        # upsample_model.add(Reshape((16, 8, 8, 1), input_shape=(1, 1024)))
        # upsample_model.add(Conv3DTranspose(2, kernel_size=(4, 3, 3), activation='relu'))
        # upsample_model.add(BatchNormalization())
        # upsample_model.add(Conv3DTranspose(4, kernel_size=(5, 3, 3), activation='relu'))
        # upsample_model.add(BatchNormalization())
        # upsample_model.add(Conv3DTranspose(2, kernel_size=(4, 3, 3), activation='relu'))
        # upsample_model.add(BatchNormalization())
        # upsample_model.add(Conv3DTranspose(1, kernel_size=(5, 3, 3), activation='relu'))
        # upsample_model.add(BatchNormalization())
        # upsample_model.add(Reshape((30, 16, 16)))
        # upsample_model.summary()


        # cnn_input = (?, 30, 16, 16, 4)
        cnn_input = Input(shape=uav_data[0].shape)
        print('input shape: ',cnn_input.shape) # (?, 30, 16, 16, 4)
        lstm_input = TimeDistributed(cnn_model)(cnn_input)
        lstm_output = lstm_model(lstm_input)
        # final_output = upsample_model(lstm_output)

        cnn_lstm_model = Model(inputs=cnn_input, outputs=lstm_output)

        def weighted_binary_crossentropy(weights):
            def w_binary_crossentropy(y_true, y_pred):
                return tf.keras.backend.mean(tf.nn.weighted_cross_entropy_with_logits(
                    y_true,
                    y_pred,
                    weights,
                    name=None
                ), axis=-1)
            return w_binary_crossentropy

        weighted_loss = weighted_binary_crossentropy(weights=4)

        def weighted_mean_squared_error(y_true, y_pred):
            return K.mean(K.square(4*(y_pred - y_true)), axis=-1)


        def recall(y_true, y_pred):
            y_true = math_ops.cast(y_true, 'float32')
            y_pred = math_ops.cast(y_pred, 'float32')
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall
       
        # cnn_lstm_model.load_weights('checkpoints/uav-01-0.11.hdf5')

        cnn_lstm_model.compile(optimizer='adadelta', loss=weighted_loss, metrics=[recall])
        # cnn_lstm_model.compile(
        #     optimizer='adadelta',
        #     loss=weighted_mean_squared_error,
        #     metrics=[metrics.mae]
        # )
        
        class LossHistory(tf.keras.callbacks.Callback):
            def on_train_begin(self, logs={}):
                self.losses = []

            def on_batch_end(self, batch, logs={}):
                if logs.get('val_recall'):
                    self.losses.append((logs.get('recall'),logs.get('val_recall')))
                else:
                    self.losses.append((logs.get('recall')))
        
        callbacks = []
        callbacks.append(
            ModelCheckpoint(
                filepath=os.path.join("checkpoints","uav-{epoch:02d}-{val_recall:.2f}.hdf5"),
                monitor='val_recall',
                mode='auto',
                save_best_only=False,
                save_weights_only=True,
                verbose=True
            )
        )
        history = LossHistory()
        callbacks.append(history)
        
        '''
        cnn_lstm_model.fit(x_train, y_train,
                    epochs=1, batch_size=32,
                    shuffle=True,
                    validation_data=(x_test, y_test),
                    callbacks=callbacks)

        import logging
        logger = logging.getLogger()
        logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)
        logging.info(history.losses)
        

        '''
        cnn_lstm_model.load_weights('checkpoints/uav-01-1.00.hdf5')
        prediction = cnn_lstm_model.predict(x_test)

        import cv2
        p = np.round(prediction)
        for i in range(30):
            cv2.imwrite('img/y{0}.png'.format(i), y_test[0][i] * 255)
            cv2.imwrite('img/p{0}.png'.format(i), p[0][i] * 255)
        


CSM = Cnn_Lstm_Model("data/trainingSets_overfit.npy", "data/groundTruths_overfit.npy")
# CSM.train()
#CSM.prediction()
# CSM.image(0)
