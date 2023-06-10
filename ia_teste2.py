import sqlite3
import tensorflow
import pandas as pd
from tensorflow import keras
import numpy as np
from sklearn.model_selection import train_test_split


conn = sqlite3.connect('IA_bd.sqlite3')

df = pd.read_sql_query("SELECT * from dados", conn)

X = df.drop(labels=['id', 'vencedor','d_brt_a', 'd_brt_b', 'pontos_a', 'pontos_b', 'dist_race'], axis=1)
y = df.vencedor

X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=2/3, random_state=1)

model = keras.Sequential([
    keras.layers.Dense(14, activation='relu', input_shape=(26,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compilar a rede neural
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Treinar a rede neural com os dados de treinamento
model.fit(X_train, y_train, epochs=500)

# Avaliar a precisão da rede neural com os dados de teste
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Precisão da rede neural:', test_acc)
probabilities = model.predict(X_test)
predictions = np.argmax(probabilities, axis=-1)
probabilities_percentages = np.vectorize(lambda p: "{:.2f}%".format(p * 100))(probabilities)
print(probabilities_percentages)
print(predictions)
