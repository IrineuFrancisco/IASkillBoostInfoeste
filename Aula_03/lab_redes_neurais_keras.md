# 🧠 Laboratório Prático: Redes Neurais Profundas com Keras — Do Perceptron ao Backpropagation

**Ambiente:** Google Colaboratory (`Python 3.10+` com GPU/CPU) & [Simulador Web de Redes Neurais](https://irineufrancisco.github.io/ExemploRedeNeural/)  
**Modalidade:** Aprendizado Profundo (*Deep Learning / Redes Neurais Artificiais Densas*)  
**Tempo Estimado:** 40 a 50 minutos  
**Dataset:** `sklearn.datasets.load_wine` (13 features físico-químicas)  
**Frameworks:** `TensorFlow`, `Keras` (`Sequential`, `Dense`, `Dropout`), `Scikit-Learn`

---

## 📋 1. ENUNCIADO DA ATIVIDADE (CONTEXTO DE NEGÓCIO)

> ### 🏭 Desafio: Superando Modelos Clássicos com Redes Neurais Artificiais
> Na Aula 01, nosso classificador supervisionado clássico (KNN) alcançou cerca de $72\%$ de acurácia no dataset de vinhos sem padronização. A diretoria da vinícola parceira do **InovaMarketplace** exige um nível de precisão superior a **$95\%$** para certificar safras de alto padrão para exportação.
>
> Para vencer as fronteiras não-lineares dos compostos químicos, você foi encarregado de projetar, compilar e treinar uma **Rede Neural Profunda (*Multilayer Perceptron — MLP*)** utilizando o framework industrial **Keras/TensorFlow**.
>
> **Sua Missão:**
> 1. Compreender o funcionamento biológico e matemático da sinapse artificial através do [Simulador Interativo Maçã vs. Laranja](https://irineufrancisco.github.io/ExemploRedeNeural/).
> 2. Construir uma arquitetura de rede neural densa com camadas ocultas (`Dense`) e funções de ativação não-lineares (`ReLU`).
> 3. Configurar a camada de saída com **Softmax** para gerar probabilidades entre as 3 safras de vinho.
> 4. Compilar o modelo com a função de perda `SparseCategoricalCrossentropy` e o otimizador adaptativo `Adam`.
> 5. Treinar a rede por 80 épocas, plotar as curvas de **Perda (*Loss*)** e **Acurácia**, e verificar a evolução do modelo até superar $96\%$ de acurácia!

---

## 🛠️ 2. PASSO A PASSO DETALHADO DO LABORATÓRIO

```mermaid
flowchart LR
    IN["Camada de Entrada\n(13 Neurônios Químicos)"] --> H1["Camada Oculta 1\n(16 Neurônios + ReLU)"]
    H1 --> H2["Camada Oculta 2\n(8 Neurônios + ReLU)"]
    H2 --> OUT["Camada de Saída\n(3 Neurônios + Softmax)"]
    OUT --> LOSS["Função de Perda\n(Crossentropy)"]
    LOSS --> BACK["Backpropagation (Adam)\n(Ajuste dos Pesos W e Bias b)"]
```

### Passo 1: O Ciclo de Vida do Aprendizado Profundo

| Etapa | Nome Técnico | O que ocorre matematicamente? |
| :--- | :---: | :--- |
| **1. Propagação Direta** | *Forward Pass* | Os dados de entrada são multiplicados pelos pesos ($W$), somados ao bias ($b$) e ativados por $\text{ReLU}(z) = \max(0, z)$. |
| **2. Medição do Erro** | *Loss Function* | A função de perda compara o vetor previsto pela Softmax com o rótulo real e calcula a penalidade numérica. |
| **3. Propagação Reversa** | *Backpropagation* | A Regra da Cadeia do Cálculo calcula o gradiente do erro em direção às camadas iniciais. |
| **4. Otimização** | *Gradient Descent (Adam)* | Os pesos sinápticos são atualizados na direção oposta ao gradiente para diminuir a perda. |

---

### Passo 2: Preparação e Padronização dos Dados
No Google Colab, importe o TensorFlow e prepare as amostras com `StandardScaler`:

```python
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

# Padronização obrigatória para Redes Neurais (evita explosão de gradientes)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Formato dos dados de treino: {X_train_scaled.shape}")
```

---

### Passo 3: Construção da Arquitetura Densa no Keras
Projetamos uma rede sequencial com 13 entradas, duas camadas densas com ReLU e 3 neurônios de saída com Softmax:

```python
# Fixando sementes para reprodutibilidade
tf.random.set_seed(42)

modelo = keras.Sequential([
    # Camada Oculta 1: 16 neurônios
    layers.Dense(16, activation='relu', input_shape=(13,), name="Camada_Oculta_1"),
    layers.Dropout(0.1),  # Desliga 10% das conexões aleatoriamente para evitar overfitting
    
    # Camada Oculta 2: 8 neurônios
    layers.Dense(8, activation='relu', name="Camada_Oculta_2"),
    
    # Camada de Saída: 3 classes com distribuição probabilística
    layers.Dense(3, activation='softmax', name="Camada_Saida_Softmax")
])

modelo.summary()
```

---

### Passo 4: Compilação e Treinamento
Configuramos a função de perda, o otimizador e treinamos por 80 épocas:

```python
modelo.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Treinamento armazenando o histórico
historico = modelo.fit(
    X_train_scaled, y_train,
    epochs=80,
    batch_size=16,
    validation_split=0.2,
    verbose=0  # Silencia saídas linha a linha
)

print(" Treinamento concluído com sucesso!")
```

---

### Passo 5: Avaliação Final e Plotagem das Curvas de Aprendizado
Avaliamos a rede no conjunto de teste e plotamos as curvas de Loss e Acurácia:

```python
# Avaliação no conjunto de teste inédito
loss_teste, acc_teste = modelo.evaluate(X_test_scaled, y_test, verbose=0)
print(f"\n==========================================")
print(f" Acurácia da Rede Neural no Teste: {acc_teste * 100:.2f}%")
print(f" Erro de Perda (Loss): {loss_teste:.4f}")
print(f"==========================================\n")

# Gráficos de Aprendizado
plt.figure(figsize=(12, 4))

# 1. Curva de Perda (Loss)
plt.subplot(1, 2, 1)
plt.plot(historico.history['loss'], label='Treino', color='#E30613')
plt.plot(historico.history['val_loss'], label='Validação', color='#1A73E8', linestyle='--')
plt.title('Evolução da Função de Perda (Loss)')
plt.xlabel('Épocas')
plt.ylabel('Erro')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Curva de Acurácia
plt.subplot(1, 2, 2)
plt.plot(historico.history['accuracy'], label='Treino', color='#10B981')
plt.plot(historico.history['val_accuracy'], label='Validação', color='#F59E0B', linestyle='--')
plt.title('Evolução da Acurácia (%)')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 🧪 3. EXPERIMENTO CIENTÍFICO: TESTES NO SIMULADOR E HIPERPARÂMETROS

### Teste 1: Calibração Manual no Simulador de Sinapses
Acesse o simulador visual criado para o curso:  
👉 **[https://irineufrancisco.github.io/ExemploRedeNeural/](https://irineufrancisco.github.io/ExemploRedeNeural/)**  
1. Tente calibrar manualmente os pesos ($w_1$, $w_2$) e o viés ($b$) para separar maçãs de laranjas.
2. Observe como é difícil encontrar os valores à mão, demonstrando a genialidade do algoritmo **Backpropagation** que encontra esses pesos automaticamente em milissegundos!

### Teste 2: O Perigo da Taxa de Aprendizado (*Learning Rate*)
No Colab, altere a taxa de aprendizado do Adam:
* `learning_rate=1.0` (MUITO ALTO): O que acontece com a curva de Loss? Ela oscila caoticamente?
* `learning_rate=0.00001` (MUITO BAIXO): A rede consegue aprender em 80 épocas ou fica "travada"?

---

## 💻 4. CÓDIGO FONTE COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

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

wine = load_wine()
X_tr, X_te, y_tr, y_te = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_tr = scaler.fit_transform(X_tr)
X_te = scaler.transform(X_te)

net = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(13,)),
    layers.Dense(8, activation='relu'),
    layers.Dense(3, activation='softmax')
])

net.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
net.fit(X_tr, y_tr, epochs=60, batch_size=16, verbose=0)

_, acc = net.evaluate(X_te, y_te, verbose=0)
print(f"Acurácia Final da Rede Neural: {acc*100:.2f}%")
```

---

## ✅ 5. ENTREGÁVEL DA ATIVIDADE (CHECKLIST DE CONCLUSÃO)

Para validar a conclusão deste laboratório, certifique-se de preencher os itens:
- [ ] Exercício executado no simulador interativo web com compreensão de pesos e bias.
- [ ] Rede neural construída no Keras com camadas densas e funções de ativação.
- [ ] Treinamento finalizado superando a marca de 95% de acurácia nos dados de teste.
- [ ] Gráfico com as curvas de aprendizado (Loss e Acurácia) gerado e analisado.
- [ ] Resposta no caderno: *Qual a função da ativação Softmax na última camada e por que a soma das suas saídas é sempre igual a 100%?*
