import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.utils import np_utils
from data.searcher import search_bidding
from data.searcher import vectorize_hand
from sklearn.model_selection import train_test_split


BIDDING = "1N,P,P,P"

df = search_bidding(BIDDING)


X = df["leader"].values
X = np.array([vectorize_hand(h) for h in X])
y = df["lead"].values
y = np.stack(np_utils.to_categorical(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def get_model():
    model = None
    # whatever
    return model

batch_size = 32
epochs = 100

model = get_model()
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=1)
score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
print("Accuracy: ", score[1]*100)