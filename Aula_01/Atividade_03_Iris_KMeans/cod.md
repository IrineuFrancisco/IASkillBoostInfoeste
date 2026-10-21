## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# PIPELINE DE APRENDIZADO NÃO SUPERVISIONADO - K-MEANS NO DATASET IRIS
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 1. Carregar os dados
df = pd.read_csv('iris.csv')
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values

# 2. Executar K-Means com K=3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)
score = silhouette_score(X, df['cluster'])

print("=== RESULTADOS DO AGRUPAMENTO NÃO SUPERVISIONADO ===")
print(f"Número de Amostras Analisadas: {len(df)}")
print(f"Coeficiente de Silhueta Médio: {score:.4f}\n")
print("Contagem por Grupo Descoberto:")
print(df['cluster'].value_counts())

# 3. Plotagem dos Clusters
plt.figure(figsize=(7, 5))
plt.scatter(df['petal_length'], df['petal_width'], c=df['cluster'], cmap='viridis', s=60, alpha=0.8)
plt.scatter(kmeans.cluster_centers_[:, 2], kmeans.cluster_centers_[:, 3], c='red', s=180, marker='X', label='Centroides')
plt.title(f"K-Means (K=3) — Flores Iris (Silhueta: {score:.2f})")
plt.xlabel("Petal Length (cm)")
plt.ylabel("Petal Width (cm)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```
