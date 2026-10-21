## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# PIPELINE COMPLETO DE CLASSIFICAÇÃO SUPERVISIONADA - DATASET VINHOS
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# 1. Carga dos dados
wine = load_wine()
X, y = wine.data, wine.target

# 2. Divisão Treino e Teste (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Pré-processamento: Padronização Z-Score
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Treinamento do Modelo com K=5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# 5. Avaliação de Desempenho
y_pred = knn.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)

print(f"=== RESULTADOS DA VINÍCOLA ===")
print(f"Acurácia Final nos Dados de Teste: {acc * 100:.2f}%\n")
print(classification_report(y_test, y_pred, target_names=wine.target_names))

# 6. Gráfico da Matriz de Confusão
plt.figure(figsize=(6, 5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=wine.target_names, yticklabels=wine.target_names)
plt.title(f"Matriz de Confusão - KNN Padronizado (Acurácia: {acc*100:.1f}%)")
plt.xlabel("Predição do Modelo")
plt.ylabel("Classe Real da Casta")
plt.tight_layout()
plt.show()
```
