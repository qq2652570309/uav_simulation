from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model

from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
# import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

uav_data = np.load("trainingSets.npy")

uav_label = np.load("groundTruths.npy")
uav_label = (uav_label - np.min(uav_label)) / np.max(uav_label) - np.min(uav_label)
print(uav_label.shape)
print(np.min(uav_label))
print(np.max(uav_label))
print(np.mean(uav_label))
print(np.median(uav_label))

(x_train, y_train) = uav_data[:850], uav_label[:850]
# y_train = y_train.reshape((850, 16, 16, 1))
(x_test, y_test) = uav_data[850:], uav_label[850:]
# y_test = y_test.reshape((150, 16, 16, 1))

input_img = Input(shape=(32, 16, 16))

x = Conv2D(16, (3, 3), activation='relu', padding='same', data_format='channels_first')(input_img)
x = MaxPooling2D((2, 2), padding='same', data_format='channels_first')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same', data_format='channels_first')(x)
x = MaxPooling2D((2, 2), padding='same', data_format='channels_first')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same', data_format='channels_first')(x)
encoded = MaxPooling2D((2, 2), padding='same', data_format='channels_first')(x)
# print('after 3rd MaxP: ', encoded.shape)

x = Conv2D(8, (3, 3), activation='relu', padding='same', data_format='channels_first')(encoded)
x = UpSampling2D((2, 2), data_format='channels_first')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same', data_format='channels_first')(x)
x = UpSampling2D((2, 2), data_format='channels_first')(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same', data_format='channels_first')(x)
x = UpSampling2D((2, 2), data_format='channels_first')(x)
decoded = Conv2D(32, (3, 3), activation='sigmoid', padding='same', data_format='channels_first')(x)
# print(decoded.shape)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

autoencoder.fit(x_train, y_train,
                epochs=20,
                batch_size=16,
                shuffle=True,
                validation_data=(x_test, y_test),
                callbacks=[TensorBoard(log_dir='./tmp/autoencoder')])

decoded_imgs = autoencoder.predict(x_test)


np.save('prediction.npy', decoded_imgs)