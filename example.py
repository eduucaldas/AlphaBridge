import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.utils import np_utils
from data.parser import search_bidding
from data.tools import categorize_hand
from sklearn.model_selection import train_test_split


BIDDING = "1N,P,P,P"

df = search_bidding(BIDDING)


X = df["leader"].values
X = np.array([categorize_hand(h) for h in X])
y = (df["lead"]//13).values
y = np.stack(np_utils.to_categorical(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def get_model():
    model = Sequential()
    model.add(Dense(256, input_dim=52, activation='relu'))
    model.add(Dense(256, input_dim=52, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

batch_size = 32
epochs = 100

model = get_model()
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=1)
score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
print("Accuracy: ", score[1]*100)
