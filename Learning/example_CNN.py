import numpy as np
from keras.models import Sequential
from keras.utils import np_utils
from data.searcher import search_bidding
from data.searcher import vectorize_hand
from sklearn.model_selection import train_test_split
from keras.layers import Conv2D, Dense, Flatten, InputLayer, Input, Reshape
from keras.utils import np_utils


BIDDING = "1N,P,P,P"

df = search_bidding(BIDDING)


X = df["leader"].values
X = np.array([vectorize_hand(h) for h in X])
y = (df["lead"]//13).values
y = np.stack(np_utils.to_categorical(y, num_classes = 4))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def get_model():
    size_flat = 52;
    shape_full = (4, 13, 1)
    num_of_chanels = 1
    num_classes = 4
    
    model = Sequential()
    model.add(InputLayer(input_shape=(size_flat,)))
    
    model.add(Reshape(shape_full))
    
    # First convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=26, padding='same',
                     activation='relu', name='layer_conv1'))
    
    # Second convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=52, padding='same',
                     activation='relu', name='layer_conv2'))
    
    # Third convolutional layer with ReLU-activation
    model.add(Conv2D(kernel_size=4, strides=1, filters=52, padding='same',
                     activation='relu', name='layer_conv3'))

    # Trying with a fourth layer
    #model.add(Conv2D(kernel_size=2, strides=1, filters=52, padding='same',
    #                 activation='relu', name='layer_conv4'))

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

epochs = 10
batch_size = 256


model = get_model()
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=1)
score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
print("Accuracy: ", score[1]*100)