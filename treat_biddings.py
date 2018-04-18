# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:32:18 2018

@author: pepou
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.utils import np_utils
from data.parser import search_biddings, leader_hand
from data.tools import categorize_hand, vectorize_hand
from data.auxiliary_functions import longest_color, strongest_color, add_color
from data.symetry import all_symetries
from data.high_low import classe8
import data.enums
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.layers import Conv2D, Dense, Flatten, InputLayer, Reshape, Dropout
from math import ceil

def translate_bid(bids):
    bid = []
    for k in range(24):
        x = [0] * 38
        x[int(bids[k])] = 1
        bid = bid + x
    return np.array(bid)

def encode_raw_biddings():
    
    df = pd.read_hdf('store.hdfs')
    south = df[["south{i}".format(i=i) for i in range(1,14)]].values
    west = df[["west{i}".format(i=i) for i in range(1,14)]].values
    north = df[["north{i}".format(i=i) for i in range(1,14)]].values
    east = df[["east{i}".format(i=i) for i in range(1,14)]].values
    bid = df[["bidding{i}".format(i=i) for i in range(1, 25)]].values
    leader = df.leader.values
    y = (df["lead"]//13).values
    leader = [np.concatenate([leader_hand(i, leader, south, west, north, east), bid[i]]) for i in range(len(leader)) if not True in np.isnan(bid[i]) and y[i] in [0, 1, 2, 3]]
    X = np.array(leader)
    y = np.array([y[i] for i in range(len(y)) if not True in np.isnan(bid[i]) and y[i] in [0, 1, 2, 3]])
    y = np_utils.to_categorical(y, num_classes = 4)
    del df
    return X, y

def get_model():
    
    size_flat = 37
    num_classes = 4
    
    model = Sequential()
    model.add(InputLayer(input_shape=(size_flat,)))
    model.add(Dropout(0.1))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(512, activation='relu'))

    # Last fully-connected / dense layer with softmax-activation
    model.add(Dense(num_classes, activation='softmax'))

    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def compile_model():
    
    X, y = encode_raw_biddings()
    
    epochs = 20
    batch_size = 256

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = get_model()
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)
    score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
    print("Accuracy: ", score[1]*100)
    
    Y_pred = model.predict(X_test)
    y_pred = np.argmax(Y_pred, axis=1)
    y_=np.argmax(y_test,axis=1)

    target_names = ['S', 'H', 'D', 'C']
    print("\nCorrélation prédiction / true:\n")
    print(classification_report(y_, y_pred,target_names=target_names))
    print(confusion_matrix(y_, y_pred))

def main():

    compile_model()    
    
    
if __name__ == '__main__':
    main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    