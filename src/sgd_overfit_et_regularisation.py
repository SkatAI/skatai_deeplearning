# -*- coding: utf-8 -*-
"""SGD Overfit et regularisation

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K0txtlDKYCZPr5LlZSkAmGJsTy1UkOtN

# SGD et overfit

Dans ce notebook nous allons entrainer un modele de gradient stochastique de scikit-learn et montrer comment detecter l'overfit

Dans un second temps nous appliquerons de la régularisation L2 pour compenser cet overfit.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle

"""# Création du dataset

Plutot que d'utiliser un vrai jeu de données, nous allons le créer avec [make_classification](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html#sklearn.datasets.make_classification) de scikit-learn.
"""

X, y = make_classification(n_samples=200, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=42)

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='k', s=50)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Scatter Plot')
plt.colorbar(label='Catégorie')
plt.show()

# Split the dataset into training and test sets with a smaller training set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

"""# Le modèle

Soit un [Stochastic Gradient Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) en veillant à supprimer la regularisation : `penalty=None`



"""

clf = SGDClassifier(penalty=None,  random_state=42, loss='log_loss')
clf

"""La fonction suivante permet de visualier l'evolution de la fonction de cout au fil des iterations


"""

def plot_loss():
    plt.figure(figsize=(8, 6))
    plt.plot(range(n_epochs), test_losses, label='Test Loss')
    plt.plot(range(n_epochs), train_losses, label='Training Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Log Loss')
    plt.title('Log Loss par Iterations')
    plt.legend()
    plt.grid()
    plt.show()

"""Plutot que d'entraîner le modele avec la fonction `fit()`, on utilise la fonction `partial_fit()` qui permet d'entrainer le modèle pas à pas pour observer son évolution à chaque itération."""

def train(X_train, y_train, X_test, y_test):
    train_losses = []
    test_losses = []

    for epoch in range(n_epochs):
        X_train, y_train = shuffle(X_train, y_train, random_state=42)

        clf.partial_fit(X_train, y_train, classes=np.unique(y))

        y_train_pred_proba = clf.predict_proba(X_train)
        y_test_pred_proba = clf.predict_proba(X_test)

        train_loss = log_loss(y_train, y_train_pred_proba)
        test_loss = log_loss(y_test, y_test_pred_proba)
        train_losses.append(train_loss)
        test_losses.append(test_loss)
    return train_losses, test_losses

def eval():
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)

    # Calculate accuracy
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    print(f'Training accuracy: {train_accuracy:.2f}')
    print(f'Test accuracy: {test_accuracy:.2f}')

"""# entrainement sans regularisation"""

n_epochs = 1000
clf = SGDClassifier(penalty=None,  random_state=42, loss='log_loss', learning_rate = 'constant', eta0 = 0.01)
train_losses, test_losses = train(X_train, y_train, X_test, y_test)
eval()
plot_loss()

"""A quoi voyez-vous que le modele overfit ?

# A vous

Ajoutez une regularisation L2 au model avec un alpha = 0.01 et observez la fonction de cout

# Que peut on faire pour reduire encore l'overfit ?

- augmenter encore la regularisation
- utiliser plus  des données pour l'entrainement
"""