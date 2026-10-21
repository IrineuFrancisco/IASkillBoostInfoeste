## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# REDE NEURAL PROFUNDA (MLP) COM TENSORFLOW/KERAS
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# Referência: Atividade_01_Redes_Neurais_Keras / Atividade.md
# ==============================================================================

# Passo 1: Preparação e Padronização dos Dados
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Carga e divisão dos dados
wine = load_wine()
X, y = wine.data, wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Padronização obrigatória para Redes Neurais
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Formato dos dados de treino: {X_train_scaled.shape}")

# Passo 2: Construção da Arquitetura Densa no Keras
tf.random.set_seed(42)

modelo = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(13,), name="Camada_Oculta_1"),
    layers.Dropout(0.1),
    layers.Dense(8, activation='relu', name="Camada_Oculta_2"),
    layers.Dense(3, activation='softmax', name="Camada_Saida_Softmax")
])

modelo.summary()

# Passo 3: Compilação e Treinamento
modelo.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

historico = modelo.fit(
    X_train_scaled, y_train,
    epochs=80,
    batch_size=16,
    validation_split=0.2,
    verbose=0
)

print("Treinamento concluído com sucesso!")

# Passo 4: Avaliação Final e Plotagem das Curvas de Aprendizado
loss_teste, acc_teste = modelo.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Acurácia no Teste: {acc_teste * 100:.2f}% | Perda (Loss): {loss_teste:.4f}")

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(historico.history['loss'], label='Treino', color='#E30613')
plt.plot(historico.history['val_loss'], label='Validação', color='#1A73E8', linestyle='--')
plt.title('Curva de Perda (Loss)')
plt.xlabel('Épocas')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(historico.history['accuracy'], label='Treino', color='#10B981')
plt.plot(historico.history['val_accuracy'], label='Validação', color='#F59E0B', linestyle='--')
plt.title('Curva de Acurácia (%)')
plt.xlabel('Épocas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```
