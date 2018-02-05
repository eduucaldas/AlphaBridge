import numpy as np

from archive_parser import archive_to_dataframe
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC


filename = "archive.dat"
df = archive_to_dataframe(filename)

X = df["player"].values.tolist()
# X = [np.ravel(np.stack(v)) for v in df[["player1", "player2", "player3", "player4"]].values]
y = (df["entame"] // 13).values.tolist()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = OneVsRestClassifier(SVC(random_state=0)).fit(X_train, y_train)
print(clf.score(X_test, y_test))
