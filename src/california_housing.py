# -*- coding: utf-8 -*-
"""California housing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q77Za5BMbztVHKPuecIz_tp8RdFaY6lN

Description du jeu de données California Housing

https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html

Le jeu de données California Housing contient les caractéristiques suivantes pour chaque échantillon de données :

    MedInc: Revenu médian des ménages dans le quartier (en dizaines de milliers de dollars).
    HouseAge: Âge médian des maisons dans le quartier.
    AveRooms: Nombre moyen de pièces par logement.
    AveBedrms: Nombre moyen de chambres à coucher par logement.
    Population: Population totale du quartier.
    AveOccup: Moyenne des occupants par logement.
    Latitude: Latitude du quartier.
    Longitude: Longitude du quartier.

Variable cible

La variable cible (ou variable à prédire) est :

    MedHouseVal: Valeur médiane des maisons dans le quartier (en centaines de milliers de dollars).
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler



df = pd.read_csv('https://raw.githubusercontent.com/SkatAI/deeplearning/master/data/housing.csv')
df.head()

df.columns

df.dropna(inplace = True)

df.shape

df.ocean_proximity.value_counts()

mapping = {
'<1H OCEAN': 0,
'INLAND': 1,
'NEAR OCEAN': 2,
'NEAR BAY': 3,
'ISLAND': 4,
}

df['op_cat'] = df.ocean_proximity.apply(lambda op : mapping[op] )
df['op_cat'].value_counts()

df = df.sample(frac = 1, random_state = 88).copy()
df.reset_index(inplace = True, drop = True)
df.head()

X = df[['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income','op_cat']]
y = df['median_house_value'].values

X.head()

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

np.min(X_scaled), np.max(X_scaled)

X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.33, random_state=42)
print(X_train.shape)
print(X_test.shape)

# Commented out IPython magic to ensure Python compatibility.
# tensorboard
# %load_ext tensorboard

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dense(64, activation = 'relu'),
    tf.keras.layers.Dense(1, activation = 'linear')
])

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics = ['mse'],
    loss = 'mse'
)

import datetime

logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

model.fit(X_train, y_train, epochs = 100, callbacks=[tensorboard_callback],     validation_data = (X_test, y_test) )

# eval
y_pred = model.predict(X_test)
y_pred[:5]

"""# evaluation"""

# overfit ?
from sklearn.metrics import mean_squared_error

y_ = model.predict(X_train)
rmse0_train = np.sqrt(mean_squared_error(y_, y_train))
print(f" rmse train : {rmse0_train} ")

from sklearn.metrics import mean_squared_error
rmse0 = np.sqrt(mean_squared_error(y_test, y_pred))
print(f" rmse : {rmse0} ")

diff0 = np.abs(y_test - y_pred[:, 0])

np.mean(diff0), np.std(diff0)

plt.hist(diff0, bins = 100);
plt.grid()



from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(
    n_estimators = 100,
    max_depth = 3,
    max_features = "sqrt",
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

from sklearn.metrics import mean_squared_error
rmse0 = np.sqrt(mean_squared_error(y_test, y_pred))
print(f" rmse : {rmse0} ")





