import cv2
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
import numpy as np

#Carregamento de um dataset de exemplo(usaremos o dataset de dígitos do sklearn)
digits = load_digits()
X = digits.images # Imagens 8x8
y = digits.target # Rótulos

# Redimensiona as imagens para o formato (8, 8, 1) (necessário para a CNN)
X = np.expand_dims(X, axis=-1)
# Divide os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#crie a camada Flatten para transformar em vetor de características que seja aceito pela MLP
def criar_cnn(input_shape):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same",
    input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same",
    input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    return model

#Chame a função CNN que você criou passando o shape para ela
X = np.expand_dims(X, axis=-1)
# Divide os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
input_shape = (8, 8, 1)
cnn_model = criar_cnn(input_shape)

# Compile a CNN
cnn_model.compile (optimizer="adam", loss = "crossentropy", metrics=["accuracy"])

# Treine a CNN
cnn_model.fit(X_train, y_train, epochs=3, batch_size=32, verbose=2)

X_train_cnn_features = cnn_model.predict(X_train)

X_test_cnn_features = cnn_model.predict(X_test)

# Cria a MLP usando a camada Flatten
mlp = MLPClassifier(hidden_layer_sizes=(100,100), max_iter=500, random_state=42)

# Treina a MLP
mlp.fit(X_train_cnn_features, y_train)

# Mede a Assertividade da MLP
y_pred = mlp.predict(X_test_cnn_features)
accuracy = accuracy_score(y_test, y_pred)

# Exibe a acuracidade
print(f"Acurácia com CNN e MLP: accuracy * 100:.2f%")