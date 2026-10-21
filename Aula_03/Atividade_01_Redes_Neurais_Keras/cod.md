## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# REDE NEURAL PROFUNDA (MLP) COM TENSORFLOW/KERAS
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 1. Carga e divisão dos dados
wine = load_wine()
X_tr, X_te, y_tr, y_te = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)

# 2. Padronização Z-Score
scaler = StandardScaler()
X_tr = scaler.fit_transform(X_tr)
X_te = scaler.transform(X_te)

# 3. Definição da Arquitetura Keras
net = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(13,), name="Oculta_1"),
    layers.Dropout(0.1),
    layers.Dense(8, activation='relu', name="Oculta_2"),
    layers.Dense(3, activation='softmax', name="Saida")
])

# 4. Compilação e Treinamento
net.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

net.fit(X_tr, y_tr, epochs=80, batch_size=16, verbose=0)

# 5. Avaliação
loss, acc = net.evaluate(X_te, y_te, verbose=0)
print(f"Acurácia Final da Rede Neural: {acc*100:.2f}% | Loss: {loss:.4f}")
```
