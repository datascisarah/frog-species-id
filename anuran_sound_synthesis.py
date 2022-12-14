#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install a pip package in the current Jupyter kernel

import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import os
import csv
# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation, Flatten, Conv2D, MaxPooling2D


# In[7]:


#read in data from folder (containing anuran calls)
#running ML algorithm for just Species

data = pd.read_csv('Frogs_MFCCs.csv', 
                           encoding = "Latin-1")


labels = np.array(data['Species'])
data = data.drop('Genus', axis = 1)
data = data.drop('Family', axis = 1)
data = data.drop('RecordID', axis = 1)

species_list = data.iloc[:, -1]
encoder = LabelEncoder()
y = encoder.fit_transform(species_list)
print(y)


scaler = StandardScaler()
X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype = float))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# In[8]:


from keras import models
from keras import layers
model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history = model.fit(X_train,
                    y_train,
                    epochs=20,
                    batch_size=128)


test_loss, test_acc = model.evaluate(X_test,y_test)
print('test_acc: ',test_acc)

predictions = model.predict(X_test)
np.argmax(predictions[0])


# In[ ]:




