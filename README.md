# uav_simulation

# installation
pip install -r requirement

# generate training data and ground truth
python main.py

# training
python train.py

# generate image
python generateImage.py


# Official tensorflow-gpu binaries are built with: 
cuda 9.0, cudnn 7 since TF 1.5; cuda 10.0, cudnn 7 since TF 1.13. 

# LSTM Path
.venv/lib/python3.5/site-packages/tensorflow/python/keras/layers/recurrent.py
