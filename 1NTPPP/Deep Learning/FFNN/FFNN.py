import numpy as np

from archive_parser import archive_to_dataframe

from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier

from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder


filename = "archive.dat"
df = archive_to_dataframe(filename)

X = np.stack(df["player"].values)
y = (df["entame"]//13).values
y = np.stack(np_utils.to_categorical(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def get_model():
    model = Sequential()
    model.add(Dense(256, input_dim=52, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=get_model, epochs=200, batch_size=5, verbose=0)
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
results = cross_val_score(estimator, X_train, y_train, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))