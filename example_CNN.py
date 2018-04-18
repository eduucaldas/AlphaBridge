import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.utils import np_utils
from data.parser import search_biddings, leader_hand
from data.tools import categorize_hand, vectorize_hand
from data.auxiliary_functions import longest_color, strongest_color, add_color
from data.symetry import all_symetries
from data.high_low import classe8
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.layers import Conv2D, Dense, Flatten, InputLayer, Reshape, Dropout
from math import ceil
import data.enums

def get_model(num_classes, size_flat = 52, shape_full = (4, 13, 1)):
    
    model = Sequential()
    model.add(InputLayer(input_shape=(size_flat,)))
    model.add(Dropout(0.1))
    
    model.add(Reshape(shape_full))
    
    # First convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=32, padding='same',
                     activation='relu', name='layer_conv1'))
    
    # Second convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=32, padding='same',
                     activation='relu', name='layer_conv2'))
    
    # Third convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=32, padding='same',
                     activation='relu', name='layer_conv3'))

    # Trying with a fourth layer
    model.add(Conv2D(kernel_size=4, strides=1, filters=32, padding='same',
                     activation='relu', name='layer_conv4'))

    # Flatten the 4-rank output of the convolutional layers
    # to 2-rank that can be input to a fully-connected / dense layer
    model.add(Flatten())
    
    # First fully-connected / dense layer with ReLU-activation
    model.add(Dense(26, activation='relu'))

    # Last fully-connected / dense layer with softmax-activation
    model.add(Dense(num_classes, activation='softmax'))

    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

    # epoch = 100; 74.54 same with epoch=200 and epoch=20;
    # batch_size=128 au lieu de 32 on passe à 77.27; batch_size 256 is best
    # with third convolutional layer and only 10 epochs, i got 81.36, and 79.09 on second try
    # globally around 80 percent accuracy
    
def compute_model(BIDDING):
    ''' Fonction de base calculant le score du réseau'''
    df = search_biddings(BIDDING)

    X = df["leader"].values
    X = np.array([categorize_hand(h) for h in X])
    y = (df["lead"]//13).values    
    y = np.stack(np_utils.to_categorical(y, num_classes = 4))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    epochs = 20
    batch_size = 256


    model = get_model(4)
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
   
def compute_model_long(BIDDING):
    df = search_biddings(BIDDING)

    X = df["leader"].values
    X = np.array([categorize_hand(h) for h in X])
    y = (df["lead"]//13).values

#######################    Sélection de certaines donnes    ####################################################   
#    Y_longest = np.array([longest_color(x) for x in X])
#    y_longest = np.argmax(Y_longest, axis=1)
#    
#    X_ = []
#    Y_ = []
#    for k in range(len(y_longest)):
#        if y_longest[k] == y[k]:
#            X_.append(X[k])
#            Y_.append(y[k])
#    X = np.array(X_)
#    y = np.array(Y_)
    
    y = np.stack(np_utils.to_categorical(y, num_classes = 4))
    
    X, y = all_symetries(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#    epochs = max(5, min(ceil(len(X_train) / 500.), 15))
    epochs = 20
    batch_size = 256


    model = get_model(4)
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

################################    Corrélations avec la longueur   ############################################   
    print("\nCorrélation prédiction / longueur :\n")
    Y_longest = np.array([longest_color(x) for x in X_test])
    print(classification_report(np.argmax(Y_longest,axis=1), y_pred,target_names=target_names))
    print(confusion_matrix(np.argmax(Y_longest,axis=1), y_pred))
    
    print("\nCorrélation longueur / vraie classe :\n")
    y_longest = np.argmax(Y_longest, axis=1)
    print(classification_report(y_, y_longest,target_names=target_names))
    print(confusion_matrix(y_, y_longest))
    
    X_ = []
    Y_ = []
    for k in range(len(y_longest)):
        if not y_longest[k] == y_[k]:
            X_.append(y_pred[k])
            Y_.append(y_[k])
    X_ = np.array(X_)
    Y_ = np.array(Y_)
    print("\nCorrélation prédiction / true lorsque true != longest:\n")
    print(classification_report(Y_, X_,target_names=target_names))
    print(confusion_matrix(Y_, X_))
    
    X_ = []
    Y_ = []
    for k in range(len(y_longest)):
        if not y_longest[k] == y_pred[k]:
            X_.append(y_pred[k])
            Y_.append(y_[k])
    X_ = np.array(X_)
    Y_ = np.array(Y_)
    print("\nCorrélation prédiction / true lorsque pred != longest:\n")
    print(classification_report(Y_, X_,target_names=target_names))
    print(confusion_matrix(Y_, X_))
    
    X_ = []
    Y_ = []
    for k in range(len(y_longest)):
        if y_[k] == y_pred[k]:
            X_.append(y_pred[k])
            Y_.append(y_longest[k])
    X_ = np.array(X_)
    Y_ = np.array(Y_)
    print("\nCorrélation prédiction / longueur lorsque pred == y_true:\n")
    print(classification_report(Y_, X_,target_names=target_names))
    print(confusion_matrix(Y_, X_))

#############################   Test couleur la plus forte  ######################################################   
#    Y_strongest = np.array([strongest_color(x) for x in X_test])
#    print(classification_report(np.argmax(Y_strongest,axis=1), y_pred,target_names=target_names))
#    print(confusion_matrix(np.argmax(Y_strongest,axis=1), y_pred))
#    
#    y_strongest = np.argmax(Y_strongest, axis=1)
#    print(classification_report(np.argmax(y_test,axis=1), y_strongest,target_names=target_names))
#    print(confusion_matrix(np.argmax(y_test,axis=1), y_strongest))
    
def compute_model_8(BIDDING):

    df = search_biddings(BIDDING)

    X = df["leader"].values
    X = np.array([categorize_hand(h) for h in X])
    y = (df["lead"]).values    
    y = np.stack(np_utils.to_categorical([classe8(lead) for lead in y], num_classes = 8))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    epochs = 20
    batch_size = 256


    model = get_model(8)
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)
    score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
    print("Accuracy: ", score[1]*100)
    
    Y_pred = model.predict(X_test)
    y_pred = np.argmax(Y_pred, axis=1)
    y_=np.argmax(y_test,axis=1)

    target_names = ['S_low', 'S_high', 'H_low', 'H_high', 'D_low', 'D_high', 'C_low', 'C_high']
    print("\nCorrélation prédiction / true:\n")
    print(classification_report(y_, y_pred,target_names=target_names))
    print(confusion_matrix(y_, y_pred))
    
def compute_model_highLow(bid):
    
    df = search_biddings(bid)

    X = df["leader"].values
    X = np.array([categorize_hand(h) for h in X])
    y = (df["lead"]).values 
    X, y = add_color(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    epochs = 10
    batch_size = 256


    model = get_model(2, 56, (4, 14, 1))
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)
    score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
    print("Accuracy: ", score[1]*100)
    
    Y_pred = model.predict(X_test)
    y_pred = np.argmax(Y_pred, axis=1)
    y_=np.argmax(y_test,axis=1)

    target_names = ['Low', 'High']
    print("\nCorrélation prédiction / true:\n")
    print(classification_report(y_, y_pred,target_names=target_names))
    print(confusion_matrix(y_, y_pred))
    

def main():
    BIDDINGS = [
                ["1N,P,P,P", "P,1N,P,P,P", "P,P,1N,P,P,P", "P,P,P,1N,P,P,P"]]
#                ["1N,P,P,P", "P,1N,P,P,P"],
#                ["1N,P,P,P"],
#                ["1N,P,2C,P,2S,P,3N,P,P,P"],
#                ["1N,P,2C,P,2H,P,3N,P,P,P"],
#                ["1N,P,3N,P,P,P", "P,1N,P,3N,P,P,P", "P,P,1N,P,3N,P,P,P", "P,P,P,1N,P,3N,P,P,P"],
#                ["1H,P,2H,P,4H,P,P,P"],
#                ["1C,P,1H,P,1N,P,P,P"],
#                ["1C,P,1S,P,1N,P,P,P"],
#                ["2N,P,3N,P,P,P"]]
#    BIDDINGS = [[x for x in data.enums.BIDSMAP]]
    for BIDDING in BIDDINGS:
        print("\n" + " - ".join(BIDDING))
        compute_model_highLow(BIDDING)




if __name__ == '__main__':
    main()