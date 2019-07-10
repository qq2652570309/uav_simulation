from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model

from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
# import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

uav_data = np.load("trainingSets.npy")
uav_data = np.transpose(uav_data,(0,2,3,1))

uav_label = np.load("groundTruths.npy")
uav_label = np.transpose(uav_label,(0,2,3,1))


uav_label = (uav_label - np.min(uav_label)) / np.max(uav_label) - np.min(uav_label)
print(uav_label.shape)
print(np.min(uav_label))
print(np.max(uav_label))
print(np.mean(uav_label))
print(np.median(uav_label))


data_size = int(len(uav_data) * 0.85)

# (x_train, y_train) = uav_data[:850], uav_label[:850]
# (x_test, y_test) = uav_data[850:], uav_label[850:]
(x_train, y_train) = uav_data[:data_size], uav_label[:data_size]
(x_test, y_test) = uav_data[data_size:], uav_label[data_size:]

# input_img = Input(shape=(16, 16, 32))
input_img = Input(shape=uav_data[0].shape)
print('input shape: ',input_img.shape)

x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)
# print('after 3rd MaxP: ', encoded.shape)

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(32, (3, 3), activation='sigmoid', padding='same')(x)
# print(decoded.shape)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

hist = autoencoder.fit(x_train, y_train,
                epochs=100,
                batch_size=16,
                shuffle=True,
                validation_data=(x_test, y_test),
                callbacks=[TensorBoard(log_dir='./tmp/autoencoder')])
print(hist.history)

decoded_imgs = autoencoder.predict(x_test)


np.save('prediction.npy', decoded_imgs)
np.save('y_test.npy', y_test)
