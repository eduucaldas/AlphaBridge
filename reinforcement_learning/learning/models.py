from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.layers import Conv2D, Flatten, Input, Reshape
from kears.layers import Conv3D
class CNN_model:
    def __init__(self, nb_layers, nb_classes):
        self.nb_layers = nb_layers
        self.asize_flat = 52
        self.shape_full = (4, 13, 1)
        self.num_of_chanels = 1
        self.num_classes = nb_classes

    def get_model(self):
        model = Sequential()
        model.add(InputLayer(input_shape=(self.asize_flat,)))
        
        model.add(Reshape(self.shape_full))
        for i in range(self.nb_layers):
            model.add(Conv2D(kernel_size=4, strides=1, filters=26, padding='same',
                             activation='relu', name='layer_conv'+str(i)))
        model.add(Flatten())
        model.add(Dense(26, activation='relu'))
        model.add(Dense(self.num_classes, activation='softmax'))
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model




def get_model():
    model = Sequential()
    model.add(Dense(256, input_dim=52, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(52, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

