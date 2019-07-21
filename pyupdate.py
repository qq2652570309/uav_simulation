from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model

from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
import matplotlib.pyplot as plt



uav_data = np.load("trainingSets.npy") # (1000, 30, 16, 16, 4)
print('uav_data: ', uav_data.shape)

uav_label = np.load("groundTruths.npy") 

# min-max normalization, (x-min) / (max-min)
uav_label = (uav_label - np.min(uav_label)) / np.max(uav_label) - np.min(uav_label)
print(uav_label.shape)
print(np.min(uav_label))
print(np.max(uav_label))
print(np.mean(uav_label))
print(np.median(uav_label))
