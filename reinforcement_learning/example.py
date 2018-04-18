import numpy as np
from keras.utils import np_utils
from data.parser import search_biddings
from data.tools import categorize_hand
from data.symetry import permute_shdc
from sklearn.model_selection import train_test_split
from learning.models import CNN_model

BIDDINGS = ["1N,P,P,P", "P,1N,P,P,P", "P,P,1N,P,P,P", "P,P,P,1N,P,P,P"]

df = search_biddings(BIDDINGS)

print(len(df)," deals")

X = df["leader"].values
X = np.array([categorize_hand(h) for h in X])
y = (df["lead"]).values
res = list(map(lambda x:permute_shdc(*x), zip(X,y)))

X = np.array([b for a in res for b in a[0]])
y = np.array([b for a in res for b in a[1]])
y = np.stack(np_utils.to_categorical(y))
print(len(X), "deals after generating equivalent deals")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

batch_size = 256
epochs = 100

model = CNN_model(3).get_model()
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2, verbose=1)
score = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
print("Accuracy: ", score[1]*100)
