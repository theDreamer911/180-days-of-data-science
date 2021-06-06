# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3.9.0 64-bit
#     name: python390jvsc74a57bd006cb67651ce969e244f20f184e33f4ddb1106793adfe07cf7ddc131c95c4012f
# ---

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

# +
url = "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv"

df = pd.read_csv(url)
# -

# df.head()

# df.shape

df['variety'].unique()

# Map the variety
variety_mapper = {'Setosa': 0, 'Versicolor': 1, 'Virginica': 1}

# Encoding
df = df.replace(variety_mapper)

# df.head()

# df.isna().sum()

feature = df.iloc[:, 0:-1]  # features/independent
target = df.iloc[:, -1]  # target/dependednt

# print("Feature shape: {}".format(feature.shape))
# print("Target shape: {}".format(target.shape))

X_train, X_test, y_train, y_test = train_test_split(
    feature, target, random_state=0)

# print("X_train shape: {}".format(X_train.shape))
# print("y_train shape: {}".format(y_train.shape))

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

X_example = np.array([[5.3, 3.7, 1.5, 0.3]])
# print("X_example shape: {}".format(X_example.shape))

prediction = knn.predict(X_example)
# print("Flowers predict: {}".format(prediction))

y_pred = knn.predict(X_test)
# print("KNN test score: {:2f}".format(knn.score(X_test, y_test)))

flower_dict = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}


def classifier(a, b, c, d):
    arr = np.array([[a, b, c, d]])
    arr = arr.astype(np.float64)
    query = arr.reshape(1, -1)
    prediction = flower_dict[knn.predict(query)[0]]
    return prediction


# classifier(6.3, 2.7, 4.9, 2.3)
